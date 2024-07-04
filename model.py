import openai
import re
import backoff
import dashscope


class Model():
    def __init__(self, model, temperature):
        self.model = model
        self.temperature = temperature

    def get_answerkey_argument(self, text):
        try:
            answer = re.findall(r'Stance(.*?)Argument', text, flags=re.DOTALL)
            answer_key = re.findall('[A-Z]', answer[0])[0]
        except Exception:
            answer_key = "None"
        argument = text.split('Argument')[-1].strip(": ")
        return answer_key, argument

    def round0_answer(self, system, question):
        prompt = self.get_round0_prompt(system, question)
        response = self.get_response(prompt)
        answer, argument = self.get_answerkey_argument(response)
        return answer, argument, f"Stance:{answer}\nArgument:{argument}"

    def round0_open_answer(self, system, question):
        prompt = self.get_round0_prompt(system, question)
        response = self.get_response(prompt).split("Answer")[-1].strip(" :：")
        return response

    def dual_debate(self, system, question, dialogs):
        prompt = self.get_dual_prompt(system, question, dialogs)
        response = self.get_response(prompt)
        answer, argument = self.get_answerkey_argument(response)
        return answer, argument, f"Stance:{answer}\nArgument:{argument}"

    def roundtable_debate(self, system, question, dialogs, debaters_num, role):
        prompt = self.get_roundtable_prompt(system, question, dialogs, debaters_num, role)
        response = self.get_response(prompt)
        answer, argument = self.get_answerkey_argument(response)
        return answer, argument, f"Stance:{answer}\nArgument:{argument}"

    def open_debate(self, system, question, dialogs):
        prompt = self.get_dual_prompt(system, question, dialogs)
        response = self.get_response(prompt)
        argument = response.split('Statement:')[-1].strip()
        if re.search(r"Agree", response):
            return argument, True
        else:
            return argument, False


class ChatModel(Model):
    def __init__(self, model, temperature):
        super().__init__(model, temperature)

    def get_round0_prompt(self, system, question):
        return [{'role': 'system', 'content': system}, {'role': 'user', 'content': question}]

    def get_dual_prompt(self, system, question, dialogs):
        prompt = [{'role': 'system', 'content': system}, {'role': 'user', 'content': question}]
        rounds = len(dialogs) // 2 * 2
        prompt += [{"role": "assistant", "content": c} if i % 2 == 0
                   else {"role": "user", "content": c} for i, c in enumerate(dialogs[-rounds:])]
        return prompt

    def get_roundtable_prompt(self, system, question, dialogs, debaters_num, role):
        rounds = len(dialogs) // debaters_num * debaters_num
        question += "".join(f"\n{d['role']}: {d['content']}" for d in dialogs[-rounds:])
        prompt = [{'role': 'system', 'content': system.format(role, role)},
                  {'role': 'user', 'content': question}]
        return prompt


class CompletionModel(Model):
    def __init__(self, model, temperature):
        super().__init__(model, temperature)

    def get_round0_prompt(self, system, question):
        return f"{system}\n{question}\nYou:"

    def get_dual_prompt(self, system, question, dialogs):
        prompt = f"{system}\n{question}\n"
        rounds = len(dialogs) // 2 * 2
        role1 = "You"
        role2 = "Opponent"
        prompt += "\n".join(f"{role1}: {d}" if i % 2 == 0 else f"{role2}: {d}" for i, d in enumerate(dialogs[-rounds:]))
        prompt += "\nYou:"
        return prompt

    def get_roundtable_prompt(self, system, question, dialogs, debaters_num, role):
        rounds = len(dialogs) // debaters_num * debaters_num
        question += "".join(f"\n{d['role']}: {d['content']}" for d in dialogs[-rounds:])
        prompt = f"{system.format(role, role)}\n{question}\n{role}:"
        return prompt


class Openai_ChatModel(ChatModel):
    def __init__(self, api_key, model, temperature):
        super().__init__(model, temperature)
        self.client = openai.OpenAI(api_key=api_key)

    @backoff.on_exception(backoff.expo, (openai._exceptions.RateLimitError, openai._exceptions.APITimeoutError, openai._exceptions.APIError))
    def get_response(self, prompt):
        responds = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            max_tokens=2048,
            temperature=self.temperature,
            frequency_penalty=0,
            presence_penalty=0)
        return responds.choices[0].message.content.strip()


class Openai_CompletionModel(CompletionModel):
    def __init__(self, api_key, model, temperature):
        super().__init__(model, temperature)
        self.client = openai.OpenAI(api_key=api_key)

    @backoff.on_exception(backoff.expo, (openai._exceptions.RateLimitError, openai._exceptions.APITimeoutError, openai._exceptions.APIError))
    def get_response(self, prompt):
        responds = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens=2048,
            temperature=self.temperature,
            frequency_penalty=0,
            presence_penalty=0)
        return responds.choices[0].text.strip()


class Baichuan_Model(ChatModel):
    def __init__(self, api_key, model, temperature):
        super().__init__(model, temperature)
        self.client = openai.OpenAI(api_key=api_key,
                                    base_url="https://api.baichuan-ai.com/v1/")

    def get_response(self, prompt):
        completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=prompt,
                        temperature=self.temperature,
                        stream=True)
        text = "".join(chunk.choices[0].delta.content for chunk in completion)
        return text


class Qwen_Model(ChatModel):
    def __init__(self, api_key, model, temperature):
        super().__init__(model, temperature)
        dashscope.api_key = api_key

    def get_response(self, prompt):
        responses = dashscope.Generation.call(self.model,
                                              messages=prompt,
                                              result_format='message',  # 设置输出为'message'格式
                                              stream=True,  # 设置输出方式为流式输出
                                              temperature=self.temperature,
                                              incremental_output=True  # 增量式流式输出
                                              )
        text = "".join(response.output.choices[0]['message']['content'] for response in responses)
        return text
