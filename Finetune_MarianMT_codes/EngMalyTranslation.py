import string
import pandas as pd
import torch
from transformers import MarianMTModel, MarianTokenizer
from sklearn.model_selection import train_test_split
from transformers import Trainer, TrainingArguments

#基于MarianMT框架的预训练模型Helsinki-NLP/opus-mt-en-mul
# 读取数据集
df = pd.read_csv('ALL\Sentence pairs in English-Malay - 2021-11-06.tsv', sep='\t')

# 使用所需数据
data = df.iloc[:, [1, 3]].values
print(data)

# 分词和预处理
def preprocess_sentences(sentences):
    return [s.lower().translate(str.maketrans('', '', string.punctuation)) for s in sentences]

english_sentences = preprocess_sentences(data[:, 0])
malay_sentences = preprocess_sentences(data[:, 1])

# 拆分训练集和测试集
trainX, testX, trainY, testY = train_test_split(english_sentences, malay_sentences, test_size=0.2, random_state=42)

# 加载预训练模型和分词器
model_name = 'Helsinki-NLP/opus-mt-en-mul'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# 准备数据
train_encodings = tokenizer(trainX, return_tensors='pt', padding=True, truncation=True, max_length=70)
train_labels = tokenizer(trainY, return_tensors='pt', padding=True, truncation=True, max_length=70).input_ids

# 创建自定义数据集类
class TranslationDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = TranslationDataset(train_encodings, train_labels)

# 定义训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# 创建 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# 训练模型
trainer.train()

# 保存模型和分词器
model.save_pretrained('./finetuned_model')
tokenizer.save_pretrained('./finetuned_model')

# 翻译函数
def translate_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=70)
    translated = model.generate(**inputs)
    translated_sentence = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return translated_sentence[0]

# 测试翻译
test_sentence = "Hi, how are you?"
print("Translation:", translate_sentence(test_sentence))
