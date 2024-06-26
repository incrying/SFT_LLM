
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers
from datasets import load_from_disk
from trl import SFTTrainer
import os

os.environ["huggingface_token"] = "YOUR_TOKEN" #llama2 models need to grant access

dataset = load_from_disk('./path_to_custom_dataset')

model_name="huggingface_llama2_models"

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

training_args = transformers.TrainingArguments(
            output_dir="./path_to_save_model",
            num_train_epochs=30,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=1,
            optim='paged_adamw_32bit',
            save_steps=0,
            logging_steps=25,
            learning_rate=1e-5,
            weight_decay=0.001,
            # fp16=kwargs['fp16'],
            # bf16=kwargs['bf16'],
            max_grad_norm=0.3,
            # max_steps=1,
            warmup_ratio=0.03,
            group_by_length=True,
            lr_scheduler_type='cosine',
        )

trainer = SFTTrainer(
    model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=512,
    args=training_args
)

trainer.train()

model.save_pretrained("./path_to_save_model")
tokenizer.save_pretrained("./path_to_save_model")