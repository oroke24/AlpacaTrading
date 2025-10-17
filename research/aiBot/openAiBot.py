from openai import OpenAI
import json

class OpenAiBot:
    def __init__(self):
        pass
    def studyStocks(self, stocks, buying_power=10):
        try:
            aiClient = OpenAI()

            response = aiClient.responses.create(
                model="gpt-5",
                input=f"""
                    Analyze the recent performance of these stocks (with price and percent_change included): {stocks}.
                    In around 200 words, explain which stocks to keep or remove and why. 
                    Include up to 1–2 additional stocks you think are strong buys if you are >90% sure and under {buying_power}.

                    Then, based on that reasoning, return ONLY valid JSON (on a new line):
                    - Array of objects with at least "symbol", "price", "percent_change"
                    - Other fields can be 0 or "n/a"
                    - Only include stocks worth buying with a trailing stop of 4-8%
                    - Use double quotes for all keys and string values
                    - Do not include explanations, markdown, or notes outside the JSON
                    - If none qualify, return []
                    - Sort by highest recommended

                    Format strictly as:
                    EXPLANATION:
                    <your explanation here>

                    JSON:
                    <your json here>
                """
            )

            text = response.output_text

            # Split explanation and JSON
            if "JSON:" in text:
                explanation, json_str = text.split("JSON:", 1)
            else:
                explanation, json_str = text, "[]"

            # Print AI explanation
            explanation = explanation.replace("EXPLANATION:", "").strip()
            print(explanation)

            # Parse JSON to final list
            stock_data = json.loads(json_str.strip())
            return stock_data

        except Exception as e:
            print(f"Error talking to AI: {e}... Returning original list of stocks")
            return stocks
            
