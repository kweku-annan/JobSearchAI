from agent.llm_agent_service import generate_recommendations
from dotenv import load_dotenv

load_dotenv()


test_job = {
    'position_title': 'Backend Engineer',
    'company': 'TechCorp',
    'skills': 'Python, FastAPI, PostgreSQL, Docker',
    'description': 'We need a backend engineer to build APIs and manage databases.'
}

recommendations = generate_recommendations(test_job)

if recommendations:
    print("✅ SUCCESS! Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   Tech: {', '.join(rec['technologies'])}")
else:
    print("❌ FAILED")