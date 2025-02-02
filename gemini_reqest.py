import pandas as pd
import google.generativeai as genai

key = ""
genai.configure(api_key=key)

df = pd.read_excel('apartmets.xlsx')

prompt = f""" Analyze the provided DataFrame of apartment listings in Kraków. Consider the following factors to identify the best offers: 
- **Price:** Lower price is generally better. 
- **Location:** 
- Central locations (e.g., "Center", "Old Town") are generally more desirable. 
- Consider proximity to amenities and transportation. 
- **Floor:**
- Higher floors often offer better views and more light. 
- Ground floors may be less desirable.
Output: a new DataFrame containing the top 20 best offers based on your analysis. Include a new column "Rank" to indicate the order of the best offers (1 being the best).
**DataFrame:** 
{df.to_markdown(index=False)} """

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
print(response.text)
