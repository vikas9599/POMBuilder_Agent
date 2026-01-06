import re
import os
import requests
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, get_system_prompt, USER_PROMPT_TEMPLATE

load_dotenv()

class LLMService:
    def __init__(self):
        pass

    def generate_pom_files(self, script_content, model, api_key=None, model_name=None, system_prompt=None, language='javascript'):
        prompt = USER_PROMPT_TEMPLATE.format(script_content=script_content)
        
        # Use provided system prompt or fallback to language-specific default
        if system_prompt:
            current_system_prompt = system_prompt
        else:
            current_system_prompt = get_system_prompt(language)
        
        try:
            if model == 'gemini':
                response = self.process_with_gemini(prompt, api_key, model_name, current_system_prompt)
            elif model == 'grok':
                response = self.process_with_grok(prompt, api_key, model_name, current_system_prompt)
            elif model == 'claude':
                response = self.process_with_claude(prompt, api_key, model_name, current_system_prompt)
            elif model == 'ollama':
                response = self.process_with_ollama(prompt, model_name, current_system_prompt)
            else:
                # Default mock response
                response = self.mock_response(script_content)
        except Exception as e:
            return {
                "test_data": f"Error processing with {model}: {str(e)}",
                "test_page": "",
                "test_script": ""
            }

        return self.parse_response(response)

    def process_with_gemini(self, prompt, api_key=None, model_name=None, system_prompt=SYSTEM_PROMPT):
        # Prefer provided key, fallback to env
        key_to_use = api_key if api_key else os.getenv("GEMINI_API_KEY")
        if not key_to_use:
            raise ValueError("API Key is required for Gemini")
        
        genai.configure(api_key=key_to_use)
        
        # Prefer provided model name, fallback to default
        model_to_use = model_name if model_name else 'gemini-2.5-flash'
        
        model = genai.GenerativeModel(model_to_use)
        
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text

    def process_with_grok(self, prompt, api_key=None, model_name=None, system_prompt=SYSTEM_PROMPT):
        key_to_use = api_key if api_key else os.getenv("XAI_API_KEY")
        if not key_to_use:
            raise ValueError("API Key is required for Grok")
        
        client = OpenAI(
            api_key=key_to_use,
            base_url="https://api.x.ai/v1",
        )

        model_to_use = model_name if model_name else "grok-beta"

        completion = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

    def process_with_claude(self, prompt, api_key=None, model_name=None, system_prompt=SYSTEM_PROMPT):
        key_to_use = api_key if api_key else os.getenv("ANTHROPIC_API_KEY")
        if not key_to_use:
            raise ValueError("API Key is required for Claude")
        
        client = Anthropic(api_key=key_to_use)
        
        model_to_use = model_name if model_name else "claude-3-5-sonnet-20240620"
        
        message = client.messages.create(
            model=model_to_use,
            max_tokens=4000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def process_with_ollama(self, prompt, model_name=None, system_prompt=SYSTEM_PROMPT):
        # Assumes Ollama is running locally on default port
        url = "http://localhost:11434/api/chat"
        # Prefer provided model name, fallback to env or default
        model_to_use = model_name if model_name else os.getenv("OLLAMA_MODEL", "llama3")
        
        payload = {
            "model": model_to_use,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']

    def mock_response(self, script_content):
        # A simple mock response to demonstrate the functionality without burning tokens or needing keys
        return """
---START_TEST_DATA---
// testData.js
export const testData = {
  signup: {
    url: '/signup',
    validUser: {
      email: 'unique.user@example.com',
      username: 'ValidUser123',
      password: 'P@sswOrd1',
      confirmPassword: 'P@sswOrd1'
    },
    invalidEmail: 'invalid-email',
    shortUsername: 'User'
  }
};
---END_TEST_DATA---

---START_TEST_PAGE---
// signupPage.js
export class SignupPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.confirmPasswordInput = page.locator('input[name="confirmPassword"]');
    this.termsCheckbox = page.locator('input[name="termsAndConditions"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.successMessage = page.locator('.success-message');
  }

  async navigate() {
    await this.page.goto('/signup');
  }

  async fillSignupForm(data) {
    if (data.email) await this.emailInput.fill(data.email);
    if (data.username) await this.usernameInput.fill(data.username);
    if (data.password) await this.passwordInput.fill(data.password);
    if (data.confirmPassword) await this.confirmPasswordInput.fill(data.confirmPassword);
    if (data.agreeToTerms) await this.termsCheckbox.click();
  }

  async submit() {
    await this.submitButton.click();
  }
}
---END_TEST_PAGE---

---START_TEST_SCRIPT---
// signup.spec.js
import { test, expect } from '@playwright/test';
import { SignupPage } from './signupPage';
import { testData } from './testData';

test('TC_FUNCTIONAL_001 - Successful User Sign Up', async ({ page }) => {
  const signupPage = new SignupPage(page);
  await signupPage.navigate();
  
  await signupPage.fillSignupForm({
    ...testData.signup.validUser,
    agreeToTerms: true
  });
  
  await signupPage.submit();
  
  await expect(page).toHaveURL('/email-verification');
  await expect(signupPage.successMessage).toBeVisible();
});
---END_TEST_SCRIPT---
"""

    def parse_response(self, response):
        test_data = ""
        test_page = ""
        test_script = ""

        # Use regex or simple string splitting to extract sections
        # Fallback to mock response if real API returns "Not implemented"
        if "integration not implemented" in response:
             response = self.mock_response("")

        data_match = re.search(r'---START_TEST_DATA---(.*?)---END_TEST_DATA---', response, re.DOTALL)
        if data_match:
            test_data = data_match.group(1).strip()

        page_match = re.search(r'---START_TEST_PAGE---(.*?)---END_TEST_PAGE---', response, re.DOTALL)
        if page_match:
            test_page = page_match.group(1).strip()

        script_match = re.search(r'---START_TEST_SCRIPT---(.*?)---END_TEST_SCRIPT---', response, re.DOTALL)
        if script_match:
            test_script = script_match.group(1).strip()

        return {
            "test_data": test_data,
            "test_page": test_page,
            "test_script": test_script
        }
