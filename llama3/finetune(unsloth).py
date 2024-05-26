from unsloth import FastLanguageModel
import json
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
import pandas as pd
from datasets import Dataset
import argparse

max_seq_length = 2048 # Supports RoPE Scaling interally, so choose any!

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("--file_path", type=str)
   args = parser.parse_args()
   return args

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/mistral-7b-bnb-4bit",
    "unsloth/mistral-7b-instruct-v0.2-bnb-4bit",
    "unsloth/llama-2-7b-bnb-4bit",
    "unsloth/gemma-7b-bnb-4bit",
    "unsloth/gemma-7b-it-bnb-4bit", # Instruct version of Gemma 7b
    "unsloth/gemma-2b-bnb-4bit",
    "unsloth/gemma-2b-it-bnb-4bit", # Instruct version of Gemma 2b
    "unsloth/llama-3-8b-bnb-4bit", # [NEW] 15 Trillion token Llama-3
    "unsloth/Phi-3-mini-4k-instruct-bnb-4bit",
] # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = None,
    load_in_4bit = True,
)

# Do model patching and add fast LoRA weights
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    max_seq_length = max_seq_length,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

def train_dataset(train_path, tokenizer):
        tokenizer = tokenizer
        train_data = []

        json_f = json.load(open(train_path))    
        for data in json_f:
            tmp = {}
            tmp['instruction'] = data['instruction']
            tmp['input'] = data['input']
            tmp['output'] = data['output']
            prompt = """### Instruction:
            {}
            
            ### Input:
            {}
            
            ### Response:
            {}"""
            EOS_TOKEN = tokenizer.eos_token
            tmp['text'] = prompt.format(tmp['instruction'], tmp['input'], tmp['output']) + EOS_TOKEN
            
            train_data.append(tmp)

        return train_data

args = parse_args()
print(args)

train_path = args.file_path
train_set = train_dataset(train_path, tokenizer)
train_df = pd.DataFrame(train_set)
dataset = Dataset.from_pandas(train_df)

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    tokenizer = tokenizer,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        num_train_epochs = 2,
        max_steps = 100,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs",
        optim = "adamw_8bit",
        seed = 3407,
    ),
)

trainer.train()

model.save_pretrained("llama_translator")
tokenizer.save_pretrained("llama_translator")