import requests
from datetime import datetime, timedelta
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
# import openai
# from openai import OpenAI
from langchain_openai import ChatOpenAI
import os


# Download required NLTK data
nltk.download('vader_lexicon')

class FinancialAdvisor:
    def __init__(self, news_api_key, openai_api_key):
        self.mf_analyzer = MutualFundNewsAnalyzer(news_api_key)
        # openai.api_key = openai_api_key
        # self.client = OpenAI(api_key=openai_api_key)
        # os.environ["OPENAI_API_KEY"] = openai_api_key

    def get_financial_advice(self, user_query, scheme_code=None):
        """
        Generate financial advice based on user query and fund analysis
        """
        try:
            # Get fund analysis and news if scheme code is provided
            fund_context = ""
            if scheme_code:
                report = self.mf_analyzer.analyze_fund_and_news(scheme_code)
                if report:
                    analyzer.print_report_summary(report)
                    print(f"\nDetailed report has been saved to JSON file")
                    fund_context = self._prepare_fund_context(report)
            
            # Prepare the prompt for GPT
            system_prompt = """You are an experienced Indian financial advisor with deep knowledge of 
            mutual funds and the Indian market. Provide advice that is:
            1. Specific to the Indian market context
            2. Compliant with SEBI regulations
            3. Conservative and risk-aware
            4. Educational and explanatory
            5. Always includes relevant disclaimers
            
            Base your advice on the provided market news and fund information if available.
            Always mention that this is algorithmic advice and users should consult with their financial advisor."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Based on the following context and query, provide financial advice:
                
                CONTEXT:
                {fund_context}
                
                USER QUERY:
                {user_query}
                
                Provide a structured response with clear sections for:
                1. Analysis of the situation
                2. Specific recommendations
                3. Risks and considerations
                4. Additional resources or next steps
                """}
            ]
            

            # response = self.client.chat.completions.create(
            #     model="gpt-4",
            #     messages=messages,
            #     temperature=0.7,
            #     max_tokens=1000
            # )
            # return response.choices[0].message['content']


            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
            ai_msg = llm.invoke(messages)
            return ai_msg.content

            
        except Exception as e:
            print(f"Error generating advice: {e}")
            return "Sorry, I couldn't generate advice at this moment. Please try again later."
    
    def _prepare_fund_context(self, report):
        """
        Prepare fund analysis and news context for GPT
        """
        context = []
        
        # Add fund details
        fd = report['fund_details']
        context.append(f"Fund Analysis for {fd['scheme_name']} ({fd['fund_house']}):")
        context.append(f"Category: {fd['category']}")
        context.append(f"Current NAV: ₹{fd['nav']}")
        
        # Add sentiment analysis
        if 'fund_house_sentiment' in report:
            fh_sentiment = report['fund_house_sentiment']
            context.append(f"\nFund House News Sentiment: {fh_sentiment['overall_sentiment']}")
            context.append(f"Average Sentiment Score: {fh_sentiment['average_score']:.2f}")
        
        if 'category_sentiment' in report:
            cat_sentiment = report['category_sentiment']
            context.append(f"\nCategory News Sentiment: {cat_sentiment['overall_sentiment']}")
            context.append(f"Average Sentiment Score: {cat_sentiment['average_score']:.2f}")
        
        # Add recent news headlines
        context.append("\nRecent Fund House News:")
        for article in report.get('fund_house_news', [])[:3]:
            context.append(f"- {article['title']} ({article['sentiment']['sentiment']})")
        
        context.append("\nRecent Category News:")
        for article in report.get('category_news', [])[:3]:
            context.append(f"- {article['title']} ({article['sentiment']['sentiment']})")
        
        return "\n".join(context)

    def get_portfolio_advice(self, scheme_codes, user_query):
        """
        Generate advice for a portfolio of mutual funds
        """
        try:
            portfolio_context = []
            
            # Analyze each fund in the portfolio
            for scheme_code in scheme_codes:
                report = self.mf_analyzer.analyze_fund_and_news(scheme_code)
                print(report)
                if report:
                    portfolio_context.append(self._prepare_fund_context(report))
            
            return portfolio_context
            # Prepare portfolio-specific prompt
            # system_prompt = """You are an experienced Indian financial advisor with deep knowledge of 
            # mutual funds and the Indian market. Provide advice that is:
            # 1. Specific to the Indian market context
            # 2. Compliant with SEBI regulations
            # 3. Conservative and risk-aware
            # 4. Educational and explanatory
            # 5. Always includes relevant disclaimers
            
            # Base your advice on the provided market news and fund information if available.
            # Always mention that this is algorithmic advice and users should consult with their financial advisor."""
            
            # messages = [
            #     {"role": "system", "content": system_prompt},
            #     {"role": "user", "content": f"""Based on the following portfolio and query, provide comprehensive advice:
                
            #     PORTFOLIO CONTEXT:
            #     {"\n\n".join(portfolio_context)}
                
            #     USER QUERY:
            #     {user_query}
                
            #     Provide a structured response with clear sections for:
            #     1. Analysis of the situation
            #     2. Specific recommendations
            #     3. Risks and considerations
            #     4. Additional resources or next steps
            #     """}
            # ]
            
            # llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
            # ai_msg = llm.invoke(messages)
            # return ai_msg.content
            
            
            
        except Exception as e:
            print(f"Error generating portfolio advice: {e}")
            return "Sorry, I couldn't generate portfolio advice at this moment. Please try again later."

class MutualFundNewsAnalyzer:

    def __init__(self, newsapi_key, bingapi_key=''):
        self.newsapi_key = newsapi_key
        self.bingapi_key = bingapi_key
        self.mf_api_url = "https://api.mfapi.in/mf/"
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        self.category_keywords = {
            'Large Cap': [
                'large cap stocks', 'blue chip stocks', 'Nifty 50',
                'market leaders', 'large cap performance'
            ],
            'Mid Cap': [
                'mid cap stocks', 'midcap market', 'Nifty Midcap',
                'mid-sized companies'
            ],
            'Small Cap': [
                'small cap stocks', 'smallcap market', 'Nifty Smallcap',
                'emerging stocks'
            ],
            'Flexi Cap': [
                'flexi cap funds', 'flexible portfolio', 'multi-cap investment',
                'flexible cap', 'dynamic portfolio'
            ],
            'Multi Cap': [
                'multi cap funds', 'multicap stocks', 'diversified portfolio',
                'across market caps', 'multi-cap strategy'
            ],
            'Hybrid': [
                'balanced funds', 'equity hybrid', 'debt hybrid',
                'asset allocation'
            ],
            'Index': [
                'index funds', 'passive funds', 'ETF tracking',
                'index tracking'
            ],
            'Debt': [
                'india bond market', 'india  fixed income', 'india  debt market', 
                'india  interest rates'
            ]
        }


    def analyze_sentiment(self, text):
        """Analyze sentiment of text using VADER"""
        if not text:
            return {'sentiment': 'neutral', 'score': 0.0}
            
        scores = self.sentiment_analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        # Determine sentiment category
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        return {
            'sentiment': sentiment,
            'score': compound_score,
            'detailed_scores': scores
        }

    def get_news(self, keywords, days=7):
        """Enhanced news fetcher with India-specific filtering"""
        try:
            indian_domains = [
                'www.moneycontrol.com',
                'economictimes.indiatimes.com',
                'm.economictimes.com',
                'www.livemint.com',
                'business-standard.com',
                'financialexpress.com',
                'bloombergquint.com',
                'ndtv.com',
                'cnbctv18.com',
                'www.timesofindia.indiatimes.com',
                'thehindubusinessline.com',
                'businesstoday.in',
                'zeebiz.com',
                'reuters.com/world/india'
            ]
            # Add India-specific terms to the query
            india_terms = 'AND (India OR NSE OR BSE OR "Indian market" OR "Indian stocks" OR "Indian mutual funds" OR "RBI")'
            base_query = ' OR '.join(f'"{keyword}"' for keyword in keywords)
            # query = f'({base_query}) {india_terms}'
            query = f'({base_query})'
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            params = {
                'q': query,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                # 'category': 'business',
                # 'language': 'en',
                'sortBy': 'relevancy',
                # 'country': 'in',
                # 'domains':  next((domain for domain in indian_domains if domain in url.lower()), None),
                # 'domains': 'moneycontrol.com,economictimes.indiatimes.com,livemint.com,business-standard.com,financialexpress.com,ndtv.com,cnbctv18.com',
                'apiKey': self.newsapi_key
            }

            response = requests.get(self.news_api_url, params=params)
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            processed_articles = []
            seen_urls = set()

            for article in articles:
                url = article.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    
                    # Combine title and description for sentiment analysis
                    text_for_sentiment = f"{article.get('title', '')} {article.get('description', '')}"
                    sentiment_analysis = self.analyze_sentiment(text_for_sentiment)
                    
                    processed_articles.append({
                        'title': article.get('title', ''),
                        'date': article.get('publishedAt', ''),
                        'description': article.get('description', ''),
                        'url': url,
                        'source': article.get('source', {}).get('name', ''),
                        'author': article.get('author', ''),
                        'sentiment': sentiment_analysis
                    })

            return processed_articles[:10]

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def get_news_old(self, keywords, days=7):
        """News fetcher using Bing News API with India location filter"""
        try:
            # Create search query
            base_query = ' OR '.join(f'"{keyword}"' for keyword in keywords)

            # Bing News API endpoint
            endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
            
            # Headers for Bing API
            headers = {
                "Ocp-Apim-Subscription-Key": self.bingapi_key
            }

            # Parameters for Bing News search
            params = {
                'q': base_query,
                'count': 10,  # Number of results
                'mkt': 'en-IN',  # Market for India
                'freshness': f'Day{days}',  # Time period
                'textDecorations': False,
                'textFormat': 'Raw'
            }

            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            articles = response.json().get('value', [])
            processed_articles = []
            seen_urls = set()

            for article in articles:
                url = article.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    
                    # Combine title and description for sentiment analysis
                    text_for_sentiment = f"{article.get('name', '')} {article.get('description', '')}"
                    sentiment_analysis = self.analyze_sentiment(text_for_sentiment)
                    
                    processed_articles.append({
                        'title': article.get('name', ''),
                        'date': article.get('datePublished', ''),
                        'description': article.get('description', ''),
                        'url': url,
                        'source': article.get('provider', [{}])[0].get('name', ''),
                        'author': None,  # Bing API doesn't provide author information
                        'sentiment': sentiment_analysis,
                        'category': article.get('category', '')
                    })

            return processed_articles[:10]

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def get_fund_details(self, scheme_code):
        """Fetch fund details from MFAPI"""
        try:
            response = requests.get(f"{self.mf_api_url}{scheme_code}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching fund details: {e}")
            return None

    def determine_fund_type(self, fund_details):
        """Determine fund category from fund details"""
        if not fund_details or 'meta' not in fund_details:
            return None
            
        scheme_name = fund_details['meta'].get('scheme_name', '').lower()
        
        if any(x in scheme_name for x in ['large cap', 'bluechip']):
            return 'Large Cap'
        elif 'mid cap' in scheme_name:
            return 'Mid Cap'
        elif 'small cap' in scheme_name:
            return 'Small Cap'
        elif 'flexi cap' in scheme_name:
            return 'Flexi Cap'
        elif 'multi cap' in scheme_name or 'multicap' in scheme_name:
            return 'Multi Cap'
        elif any(x in scheme_name for x in ['hybrid', 'balanced', 'asset allocation']):
            return 'Hybrid'
        elif any(x in scheme_name for x in ['index', 'nifty', 'sensex']):
            return 'Index'
        elif any(x in scheme_name for x in ['debt', 'bond', 'gilt', 'credit']):
            return 'Debt'
        else:
            return 'Other'


    def get_fund_house_news(self, fund_house, days=7):
        """Get India-specific news for fund house"""
        keywords = [
            f"Indian {fund_house}",
            f"{fund_house} mutual fund India",
            f"{fund_house} AMC India",
            f"{fund_house} asset management India",
            f"{fund_house} mutual fund",
            f"{fund_house} asset management",
            f"{fund_house}"
        ]
        return self.get_news(keywords, days)

    def get_category_news(self, category, days=7):
        """Get news for a specific fund category"""
        if category not in self.category_keywords:
            return []
        return self.get_news(self.category_keywords[category], days)

    def calculate_overall_sentiment(self, articles):
        """Calculate overall sentiment from a list of articles"""
        if not articles:
            return {
                'overall_sentiment': 'neutral',
                'average_score': 0.0,
                'sentiment_distribution': {
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0
                }
            }
            
        # Calculate average sentiment score
        total_score = sum(article['sentiment']['score'] for article in articles)
        avg_score = total_score / len(articles)
        
        # Count sentiments
        sentiment_counts = {
            'positive': sum(1 for article in articles if article['sentiment']['sentiment'] == 'positive'),
            'negative': sum(1 for article in articles if article['sentiment']['sentiment'] == 'negative'),
            'neutral': sum(1 for article in articles if article['sentiment']['sentiment'] == 'neutral')
        }
        
        # Determine overall sentiment
        if avg_score >= 0.05:
            overall = 'positive'
        elif avg_score <= -0.05:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'average_score': avg_score,
            'sentiment_distribution': sentiment_counts
        }

    def print_report_summary(self, report):
        """Enhanced print summary with sentiment analysis"""
        if not report:
            print("No report available")
            return

        print("\nFund Analysis and News Report")
        print("=" * 80)
        
        # Fund Details
        fd = report['fund_details']
        print("\nFund Details:")
        print(f"Name: {fd['scheme_name']}")
        print(f"Fund House: {fd['fund_house']}")
        print(f"Category: {fd['category']}")
        print(f"Latest NAV: {fd['nav']}")
        
        # Fund House News
        print("\nFund House News and Sentiment:")
        print("=" * 80)
        
        fund_house_sentiment = report.get('fund_house_sentiment', {})
        if fund_house_sentiment:
            print(f"Overall Sentiment: {fund_house_sentiment.get('overall_sentiment', 'N/A')}")
            print(f"Average Sentiment Score: {fund_house_sentiment.get('average_score', 0):.2f}")
            print("\nSentiment Distribution:")
            distribution = fund_house_sentiment.get('sentiment_distribution', {})
            for sentiment, count in distribution.items():
                print(f"{sentiment.capitalize()}: {count}")
        
        print("\nNews Articles:")
        for i, article in enumerate(report.get('fund_house_news', []), 1):
            print(f"\n{i}. {article['title']}")
            print(f"Date: {article['date'][:10]} | Source: {article['source']}")
            if 'sentiment' in article:
                print(f"Sentiment: {article['sentiment']['sentiment']} "
                      f"(Score: {article['sentiment']['score']:.2f})")
            if article.get('description'):
                print(f"Description: {article['description']}")
            print(f"Link: {article['url']}")
            print("-" * 80)
        
        # Category News
        print(f"\nCategory News and Sentiment ({fd['category']}):")
        print("=" * 80)
        
        category_sentiment = report.get('category_sentiment', {})
        if category_sentiment:
            print(f"Overall Sentiment: {category_sentiment.get('overall_sentiment', 'N/A')}")
            print(f"Average Sentiment Score: {category_sentiment.get('average_score', 0):.2f}")
            print("\nSentiment Distribution:")
            distribution = category_sentiment.get('sentiment_distribution', {})
            for sentiment, count in distribution.items():
                print(f"{sentiment.capitalize()}: {count}")
        
        print("\nNews Articles:")
        for i, article in enumerate(report.get('category_news', []), 1):
            print(f"\n{i}. {article['title']}")
            print(f"Date: {article['date'][:10]} | Source: {article['source']}")
            if 'sentiment' in article:
                print(f"Sentiment: {article['sentiment']['sentiment']} "
                      f"(Score: {article['sentiment']['score']:.2f})")
            if article.get('description'):
                print(f"Description: {article['description']}")
            print(f"Link: {article['url']}")
            print("-" * 80)

    def analyze_fund_and_news(self, scheme_code, days=15):
        """Enhanced analysis with sentiment"""
        fund_details = self.get_fund_details(scheme_code)
        if not fund_details:
            return None

        fund_type = self.determine_fund_type(fund_details)
        fund_house = fund_details['meta'].get('fund_house')

        # Get news with sentiment
        fund_house_news = self.get_fund_house_news(fund_house, days)
        category_news = self.get_category_news(fund_type, days) if fund_type else []

        # Calculate overall sentiment for both categories
        fund_house_sentiment = self.calculate_overall_sentiment(fund_house_news)
        category_sentiment = self.calculate_overall_sentiment(category_news)

        report = {
            'fund_details': {
                'scheme_code': scheme_code,
                'scheme_name': fund_details['meta'].get('scheme_name'),
                'fund_house': fund_house,
                'category': fund_type,
                'scheme_type': fund_details['meta'].get('scheme_type'),
                'nav': fund_details['data'][0].get('nav') if fund_details.get('data') else None,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'fund_house_news': fund_house_news,
            'fund_house_sentiment': fund_house_sentiment,
            'category_news': category_news,
            'category_sentiment': category_sentiment
        }

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f'fund_analysis_{scheme_code}_{timestamp}.json'
        # with open(filename, 'w', encoding='utf-8') as f:
        #     json.dump(report, f, indent=4, ensure_ascii=False)

        return report
    

# Example usage
if __name__ == "__main__":
    NEWS_API_KEY = "a4fa3195e0c04cd9a0b139c578862932"
    analyzer = MutualFundNewsAnalyzer(NEWS_API_KEY)
    
    # Example: ICICI Retirement fund
    scheme_code = "112656"
    
    print(f"Analyzing fund {scheme_code}...")
    # report = analyzer.analyze_fund_and_news(scheme_code)
    
    # if report:
    #     analyzer.print_report_summary(report)
    #     print(f"\nDetailed report has been saved to JSON file")

    OPENAI_API_KEY = ""
    advisor = FinancialAdvisor(NEWS_API_KEY, OPENAI_API_KEY)

    query = "I'm considering investing in this fund for long-term wealth creation. What should I consider?"
    advice = advisor.get_financial_advice(query, "100631")  # HDFC Top 100 Fund
    print(advice)