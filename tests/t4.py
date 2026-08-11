from app.database.database import SessionLocal
from app.agents.recommendation_agent_v2 import recommendation_agent_v2

db = SessionLocal()
try:
    result = recommendation_agent_v2.invoke({
        "user_id": 4,
        "limit": 5,
    })

    print("\n" + "=" * 80)
    print("SMARTRECO — RECOMMENDATION AGENT V2 TEST (USER 4)")
    print("=" * 80)

    # CANDIDATES
    candidates = result.get("candidates", [])
    if candidates:
        print("\n" + "-" * 80 + "\nCANDIDATES\n" + "-" * 80)
        for c in candidates:
            p = c["product"]
            print(f"ID: {p.id:<4} | Title: {p.title:<35} | Semantic: {c.get('semantic_score', 0.0):.4f}")

    # HYBRID RANKING
    ranked = result.get("ranked_recommendations", [])
    if ranked:
        print("\n" + "-" * 80 + "\nHYBRID RANKED RECOMMENDATIONS\n" + "-" * 80)
        for rank, item in enumerate(ranked, start=1):
            p = item["product"]
            print(f"Rank {rank}: ID {p.id:<4} {p.title:<35}")
            print(f"  Behavioral: {item.get('behavioral_score', 0.0):.4f} | Semantic: {item.get('semantic_score', 0.0):.4f} | Preference: {item.get('preference_score', 0.0):.4f} | FINAL: {item.get('final_score', 0.0):.4f}\n")

    # AI RECOMMENDATION
    rec = result.get("ai_recommendation")
    print("=" * 80 + "\nAI GENERATED RECOMMENDATION\n" + "=" * 80)
    if isinstance(rec, dict):
        print(f"Product ID : {rec.get('product_id')}")
        print(f"Title      : {rec.get('title')}")
        print(f"Reason     : {rec.get('reason')}")
        print(f"Confidence : {rec.get('confidence')}")

finally:
    db.close()