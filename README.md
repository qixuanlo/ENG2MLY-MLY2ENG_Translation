**基于 MarianMT 模型的马来文-英文翻译系统**

组员分工：许凯喨（数据集、模型训练、界面、报告），罗啟轩（模型选择、选择数据集、训练模型、界面、报告），谭昀希（报告、汇报ppt）

**摘要**

  在本次作业中，我们选取了MarianMT作为我们马来文 - 英文翻译系统的基座模型，并用马来文 - 英文翻译数据集(Sentence pairs eng-malay数据集)微调MarianMT从而得到了我们的马来文 - 英文翻译系统。最终，我们也是用Qt设计了一个用户界面，可以方便用户去做马来文 - 英文翻译。

**引言**

  在如今大模型的时代，翻译任务其实是已经很好地被大模型解决了。那为什么我们还想实现翻译系统呢？我们想实现马来文 - 英文翻译系统的第一个原因就是如今的大部分翻译系统和大模型都是需要连网才能去访问它们的。所以，我们想做一个不用联网就可以用到的翻译系统。让用户可以更加方便的就实现实时翻译。此外，我们想实现马来文 - 英文翻译系统的第二个原因就是我们希望该模型是比较小的，这样用户就可以比较快速开启我们的翻译系统来进行马来文和英文直接之间的翻译。当然，小模型肯定也是有一些的局限性的，如在面对用户输入时语法没有那么的好时，可能翻译出来的效果也不会太好。其次就是我们本次实验找的数据有限，因为很少专业人士去实现马来文的翻译数据集。因此，我们的数据集比较小，然而训练出来模型的效果也只是一般般。但是，模型可以实现马来文 - 英文离线实时翻译已经是一个很大的突破了。

**方法**

MarianMT介绍：
	MarianMT是由 MarianNMT 团队开发的，他是基于 Transformer 架构的开源神经机器翻译框架。它的设计目标是高效且灵活，能够支持多种语言对的翻译任务。
	为什么选择MarianMT作为本次实验的基座模型呢？第一个原因是因为它是用了Transformers的encoder-decoder架构来实现的，encoder-decoder架构在翻译任务上通常表现更好。第二个原因就是它的参数量相对于gpt3、llama等大模型是比较小的。第三个原因就是他是已经用了100多种语言数据预训练过了的模型，我们相信他在预训练的时候已经有很好的语言基础了。
	本次实验是用了MarianMT在huggingface上的opus-mt系列来实现本次的翻译系统，系列中主要调用到的模型就是opus-mt-mul-en以及opus-mt-en-mul模型。

Sentence pairs数据集介绍：
	Sentence pairs 数据集是一种专门用于机器翻译的双语并行语料库。数据集中每条数据都是包含了两种语言的句子对，其中每对句子分别是原始语言（源语言）和目标语言的翻译。在这里我们是选择了英文到马来文的sentence pairs数据集。这种双语并行的数据集对于训练和评估机器翻译模型任务是比较容易预处理的。

**实验**

实验步骤：
1.读取数据集，并对数据进行分词以及预处理。
2.将数据处理好的数据拆分训练集和测试集。
3.加载预训练模型opus-mt-mul-en和opus-mt-en-mul以及它们相应的分词器。
4.让tokenizer编码处理好的数据。
5.将原本数据的类型转换成Dataset类。
6.定义训练参数和创建 Trainer。
7.微调MarianMT模型，并保存微调好的模型。
8.测试微调好的模型。
9.为了让用户可以更轻松地使用我们的马来文 - 英文翻译系统，我们也是简单的设计了一个Qt界面来让用户可以使用到我们的翻译系统，如图1所示。

实验结果：


图1 

![image](https://github.com/qixuanlo/ENG2MLY-MLY2ENG_Translation/assets/143249443/65d6563b-a7ad-4cdd-ab76-66ad0df1bbe0)


图2

![image](https://github.com/qixuanlo/ENG2MLY-MLY2ENG_Translation/assets/143249443/8a17c46d-a998-4c58-a559-332f271e65bb)

如图1和图2所示，我们的模型的翻译效果还是可以的。接着，我们用以下随机写的10个句子来测试我们的模型，以及在gpt4o、llama3以及Copilot上翻译这10个句子。

| 句子\模型                         | 我们的马来文-英文翻译模型         | GPT3.5                                  | llama3-8B                                        | Copilot                                 |
| --------------------------------- | --------------------------------- | --------------------------------------- | ------------------------------------------------ | --------------------------------------- |
| Saya baik, terima kasih.          | i am ok, thank you.               | I am fine, thank you.                   | I'm fine, thank you.                             | I’m fine, thank you.                    |
| Nama saya John.                   | my name is john.                  | My name is John.                        | My name is John.                                 | My name is John.                        |
| Saya dari Malaysia.               | i am from malaysia.               | I am from Malaysia.                     | I am from Malaysia.                              | I am from Malaysia.                     |
| Saya lapar.                       | i am hungry.                      | I am hungry.                            | I'm hungry.                                      | I am hungry.                            |
| Saya ingin pergi ke pantai.       | i want to go to the beach.        | I want to go to the beach.              | I want to go to the beach.                       | I want to go to the beach.              |
| I like to eat nasi lemak.         | saya suka makan nasi lemak.       | Saya suka makan nasi lemak.             | Saya suka makan nasi lemak.                      | Saya suka makan nasi lemak.             |
| Where is my car?                  | di mana kereta saya?              | Di mana kereta saya?                    | Di mana kenderaan saya?                          | Di mana kereta saya?                    |
| Can you help me?                  | bolehkah awak membantu saya?      | Tolong saya boleh?                      | Bolehkah anda bantu saya?                        | Bolehkah anda membantu saya?            |
| We go to school by bus.           | kami pergi ke sekolah dengan bus. | Kami pergi ke sekolah dengan bas.       | Kami pergi ke sekolah dengan bas.                | Kami pergi ke sekolah dengan bas.       |
| He plays soccer with his friends. | dia bermain bola dengan kawanya.  | Dia bermain bola sepak dengan kawannya. | Beliau bermain bola sepak dengan rakan-rakannya. | Dia bermain bola sepak dengan kawannya. |


表1

  从表1中可以看出除了大小写的差别以外，其实我们的马来文 - 英文翻译系统的翻译效果是和GPT3.5以及Copilot翻译的效果没有太大的区别的。

| 句子\模型                                                    | 我们的马来文-英文翻译模型                                    | GPT3.5                                                       | llama3-8B                                                    | Copilot                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Walaupun cuaca di luar begitu panas, tetapi angin sepoi-sepoi yang bertiup dari laut memberikan kesejukan kepada penduduk kampung yang sedang bekerja di ladang padi. | even the air is so hot out but the sepoi winds of the sepoi did out of the sea study to the tryers working in the good study | Even though the weather outside is very hot, the gentle breeze blowing from the sea provides coolness to the villagers working in the rice fields. | Although the weather outside is very hot, but the gentle breeze blowing from the sea brings a sense of coolness to the villagers who are working in the rice fields. | Even though the weather outside is scorching hot, the gentle breeze blowing in from the sea provides comfort to the villagers who are working in the rice fields. |
| Dalam kegelapan malam yang sunyi, gemuruh ombak yang menghempas pantai memberikan perasaan takut kepada penduduk kampung yang tinggal di tepi laut. | in the slender night of ourdays, a fluent walk of the masonry make a terromant of the ourmens lived on the nast time | In the quiet darkness of the night, the roar of the waves crashing against the shore instilled fear in the villagers living by the sea. | In the dark and quiet night, the crashing of waves against the shore gives a feeling of fear to the villagers who live by the sea. | In the silent darkness of the night, the crashing waves on the shore evoke fear in the villagers who reside by the sea. |
| Dengan berbekalkan semangat kejiranan yang tinggi, penduduk kampung itu bersatu padu membina rumah bagi keluarga yang terkena musibah kebakaran. | By concerning a lot of his his his his his hiss think the study of the village is one study to how a house for the arritors | Armed with a strong sense of community spirit, the villagers united to build a house for the family affected by the fire. | With high neighborhood spirit, the villagers came together to build a house for the family affected by the fire disaster. | With a strong sense of community spirit, the villagers came together to build houses for the families affected by the disaster. |
| Despite the scorching heat outside, the gentle breeze blowing in from the sea provided relief to the villagers working in the rice fields. | bahawa bahasa ini terbang di luar, anin yang lebih menyukup dari laut membuat lebih lebih menyelesahkan untuk pemurang yang bekerja di laman aris. | Walaupun panas terik di luar, angin sepoi-sepoi yang bertiup dari laut memberikan kelegaan kepada penduduk kampung yang bekerja di sawah padi. | Walaupun cuaca di luar begitu panas, angin sepoi-sepoi yang bertiup dari laut memberikan kesejukan kepada penduduk kampung yang sedang bekerja di ladang padi. | Walaupun cuaca di luar begitu panas, tetapi angin sepoi-sepoi yang bertiup dari laut memberikan kesejukan kepada penduduk kampung yang sedang bekerja di ladang padi. |
| In the silent darkness of the night, the roar of the waves crashing against the shore instilled fear in the villagers living by the sea. | Dalam gelap ditinggit bahasa ini, berhujuh dalam banyak sedang menyukupkan takut di dalam pempuman yang tidak laut. | Dalam kegelapan malam yang sunyi, gemuruh ombak yang menghempas pantai menimbulkan rasa takut kepada penduduk kampung yang tinggal di tepi laut. | Di gelap malam yang sunyi, gemuruh ombak yang menghempas pantai mengisytirahatkan takut kepada penduduk kampung yang tinggal di tepi laut. | Dalam kegelapan malam yang sunyi, gemuruh ombak yang menghempas pantai memberikan perasaan takut kepada penduduk kampung yang tinggal di tepi laut. |
| Armed with a strong sense of community spirit, the villagers rallied together to rebuild homes for the families affected by the fire. | sedang mereka sedang menyingkat sesuatu komunitas dan mereka bekerja untuk membangkitkan perkara untuk perkara keluarga yang mempunyai api itu. | Dengan berbekalkan semangat kejiranan yang tinggi, penduduk kampung itu bersatu padu untuk membina semula rumah bagi keluarga-keluarga yang terjejas akibat kebakaran. | Dengan berbekalkan semangat kejiranan yang kuat, penduduk kampung itu bersatu padu membina rumah bagi keluarga yang terkena musibah kebakaran. | Dengan semangat kejiranan yang tinggi, penduduk kampung bersatu padu untuk membina semula rumah bagi keluarga yang terkena musibah kebakaran. |

表2

对于表2，我们的模型，在长文本的翻译上效果没有短文本的翻译来的好，经过了分析之后，我们发现可能是训练的数据是偏向于短文本的。因此我们的短文本翻译是做得比较好的。现在马来文翻译的数据集还是比较难找的。如果在未来有机会，我们会找更多的长文本来训练模型。使模型在长文本的翻一下也是和短文本的效果一样好。

**结论**

  经过本次大作业，我们是学会了怎么筛选高质量数据以及下载调用、微调大模型，并将我们的大模型和Qt结合设计出一个用户界面。对于我们的马来文 - 英文翻译系统。如果未来有机会，我们还是会把基座模型替换成现在主流的大模型的，而且也会加入跟多的语言来进行翻译。其实本次实验中我们也是尝试了翻译一些中文和马来文的SFT数据集，也是用Superfiltering方法筛选了高质量的数据集，但是用该SFT数据集去微调量化版的llama3-8B模型之后发现翻译的效果其实没有这个MarianMT的效果来得好，所以我们才没有将llama3-8B微调的结果展现出来。但是，我们也是会把微调得到的llama-translator提交上去，毕竟也是我们的一个成果。最后，对于马来文的数据还是比较少的，而且选择什么样的模型来作为本次大作业的模型也是一种挑战，而且这次我们也是尝试了微调过llama3-8B。所以，相信这次大作业也是让我们组的每一个成员都有一些收获和成长。
