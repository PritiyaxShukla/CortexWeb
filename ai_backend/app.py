from flask import Flask, request, jsonify
from flask_cors import CORS
from summary import TextSummarizer
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from question_answer import QuestionAnswer
import os
import time
import shutil

summarizer = TextSummarizer()
app = Flask(__name__)
CORS(app)

qans = None
history = []

@app.route('/scrape', methods=['POST'])
def scrape():
    global qans
    data = request.get_json()
    url = data.get('url')
    print(f"[INFO] Received URL: {url}")

    if history and history[0] == url:
        print("[INFO] URL already scraped. Skipping scraping.")
        return jsonify({"message": "URL already scraped. Skipping scraping."})

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ))

        page = context.new_page()
        print("[INFO] Navigating to the page...")
        page.goto(url, timeout=120000, wait_until="domcontentloaded")
        time.sleep(5)

        print("[INFO] Scrolling the page to load content...")
        page.evaluate("""() => {
            return new Promise(resolve => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= document.body.scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        }""")
        time.sleep(2)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text(separator='\n', strip=True)

    os.makedirs('ai_backend', exist_ok=True)
    with open('ai_backend/scraped_output.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    if os.path.exists('faiss_db'):
        shutil.rmtree('faiss_db')

    print("[INFO] Reinitializing QuestionAnswer with new data...")
    qans = QuestionAnswer()
    history.clear()
    history.append(url)
    print("[SUCCESS] Scraping and vector DB creation completed.")
    return jsonify({"message": "Scraping and vector DB creation completed."})

@app.route('/reset', methods=['POST'])
def reset_history():
    global history, qans
    history.clear()
    qans = None
    print("[INFO] History has been cleared and scraping will restart.")
    return jsonify({"message": "History reset successfully."})

@app.route('/summary', methods=['GET'])
def get_summary():
    print("Generating summary...")
    result = summarizer.summarize_file("ai_backend/scraped_output.txt")
    print("Summary generated successfully.")
    return jsonify({"summary": result})

@app.route('/qa', methods=['GET'])
def question_ans():
    global qans
    question = request.args.get("question")
    print("Received question:", question)

    if not question:
        return jsonify({"error": "No question provided"}), 400

    if qans is None:
        filepath = 'ai_backend/scraped_output.txt'
        if not os.path.exists(filepath):
            return jsonify({"error": "Scraped data not found. Please run /scrape first."}), 400
        qans = QuestionAnswer()

    answer = qans.run_qa(question, k=5)
    print("[SUCCESS] Answer generated successfully.")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(port=5000, debug=True)




