from openai import OpenAI
import json

class OpenAiBot:
    def __init__(self):
        pass
    def studyStocks(self, stocks):
        try:
            aiClient = OpenAI()
            responseToPrint = aiClient.responses.create(
                model = "gpt-5",
                input = f"Do a study on the recent performance of these stocks and in less than 200 words, mention which to remove, keep, and why (feel free to add 1 or 2 that my filters may have missed, but only if your over 90% sure about it): {stocks}."
            )
            print(responseToPrint.output_text)

            responseToReturn = aiClient.responses.create(
                model = "gpt-5",
                input=f"""
                    Analyze these stocks: {stocks}.
                    Select only the ones worth buying if they will be traded tomorrow with a trailing stop loss of 8%.
                    Return ONLY valid JSON — an array of objects, each with the same keys as provided.
                    - Do not add explanations, markdown, or notes.
                    - Use double quotes around all keys and string values.
                    If none qualify, return [].
                    """
            )
            text = responseToReturn.output_text
            stock_data = json.loads(text)
            return stock_data
        except Exception as e:
            print(f"Error talking to AI: {e}... Returning original list of stocks")
            return stocks
            
