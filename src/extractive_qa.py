# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/tuwien-information-retrieval/air-2022-group-28/blob/main/src/extractive_qa.ipynb

# AIR - Exercise in Google Colab

## Colab Preparation

Open via google drive -> right click: open with Colab

**Get a GPU**

Toolbar -> Runtime -> Change Runtime Type -> GPU

**Mount Google Drive**

* Download data and clone your github repo to your Google Drive folder
* Use Google Drive as connection between Github and Colab (Could also use direct github access, but re-submitting credentials might be annoying)
* Commit to Github locally from the synced drive

**Keep Alive**

When training google colab tends to kick you out, This might help: https://medium.com/@shivamrawat_756/how-to-prevent-google-colab-from-disconnecting-717b88a128c0

**Get Started**

Run the following script to mount google drive and install needed python packages. Pytorch comes pre-installed.
"""

from google.colab import drive
import pandas as pd
drive.mount('/content/drive')

!pip install transformers

path="/content/drive/MyDrive/AIR/AIR/air-exercise-2/Part-3/"

qa_tuples = pd.read_csv(r'{}msmarco-fira-21.qrels.qa-tuples.tsv'.format(path),sep='8921349812748}',header=None,names=['entry'])
qa_tuples.entry = qa_tuples.entry.str.split('\t')
def fix_tuples(row):
    return [row[0],row[1],row[2],row[3],row[4],row[6:]]

qa_tuples.entry = (qa_tuples.entry.apply(fix_tuples))
qa_tuples = pd.DataFrame(qa_tuples["entry"].to_list(), columns=['queryid', 'documentid', 'relevance_grade', 'query_text', 'document_text', 'text_selection'])

def str_start(row):
    start_index = []
    for string in row.text_selection:
        start_index.append(row.document_text.index(string))
    return {'answer_start':start_index,'text':row.text_selection}

qa_tuples['answers'] = qa_tuples.apply(str_start,axis=1)

from transformers import AutoModelForQuestionAnswering,  AutoTokenizer, pipeline

model_name = "deepset/minilm-uncased-squad2"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'Why is model conversion important?',
    'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
}
res = nlp(QA_input)

print(res)

def get_answers(row):
  question = row.query_text
  context = row.document_text

  QA_input = {
    'question': question,
    'context': context
  } 

  return nlp(QA_input)['answer']

qa_tuples['model_answer'] = qa_tuples.apply(get_answers,axis=1)

from core_metrics import normalize_answer,get_tokens,compute_exact,compute_f1

def calculate_answer_scores(data):

  real_answers = data['text_selection']
  model_answer = data['model_answer']


  f1_scores = []
  exact_scores = []
  contained = []

  for answer in real_answers:
    f1_scores.append(compute_f1(answer,model_answer))
    exact_scores.append(compute_exact(answer,model_answer))
    
    if answer in model_answer:
      contained.append(1)
    else: 
      contained.append(0)
      

  return max(f1_scores),max(exact_scores),max(contained)

qa_tuples[['F1_score','Exact_score',"Contained"]] = qa_tuples.apply(calculate_answer_scores,axis=1, result_type='expand')

qa_tuples

def summarize_results(data):

  print(data.Exact_score.sum())
  print(data.Contained.sum())
  print(data.F1_score.sum()/data.shape[0])

summarize_results(qa_tuples)

qa_tuples.to_csv('{}Model_answers.csv'.format(path))

qa_tuples.shape[0]

