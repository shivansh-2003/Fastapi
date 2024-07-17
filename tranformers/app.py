from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

app = FastAPI()

# Example models
qa_model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
translation_model_name = "Helsinki-NLP/opus-mt-en-fr"

# Initialize models
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
translation_pipeline = pipeline(task="translation", model=translation_model_name, src="en", tgt="fr")


class QuestionAnsweringRequest(BaseModel):
    question: str
    context: str


class TranslationRequest(BaseModel):
    text: str


### Define Endpoints ###

@app.post("/qa")
async def question_answering(request: QuestionAnsweringRequest):
    try:
        inputs = qa_tokenizer.encode_plus(request.question, request.context, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]

        outputs = qa_model(**inputs)
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1
        answer = qa_tokenizer.convert_tokens_to_string(qa_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate")
async def translate(request: TranslationRequest):
    try:
        translated_text = translation_pipeline(request.text)[0]["translation_text"]
        return {"translation": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
