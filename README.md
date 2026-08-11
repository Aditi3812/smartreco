# 🚀 SmartReco: AI-Powered Hybrid Recommendation Engine

SmartReco is an advanced, production-grade personalized recommendation engine built for modern online learning platforms. It combines real-time user behavioral tracking, high-dimensional vector search, multi-factor hybrid scoring, stateful LangGraph agentic workflows, and Large Language Model (LLM) reasoning to deliver accurate, context-aware, and highly personalized course recommendations.

---

## 📐 System Architecture

```mermaid
graph TD
    Client[Web Client / UI / REST API] --> |Events & Views| EventRouter[Event & Product Router]
    EventRouter --> |Log Behavioral Events| EventService[Event Tracking Service]
    EventService --> |Persist Raw Events| DB[(PostgreSQL DB)]
    
    EventService --> |Trigger Interaction Memory| InteractionService[Product Interaction Service]
    EventService --> |Trigger Behavior Profile| BehaviorService[Behavior Profile Service]
    
    InteractionService --> |Update Recency & Score| DB
    BehaviorService --> |Update Category/Difficulty/Intent| DB
    
    Client --> |Get Recommendations| RecRouter[Recommendation Router]
    RecRouter --> |Invoke Workflow| RecAgent[LangGraph Recommendation Agent v2]
    
    subgraph Agentic Orchestration [LangGraph Agent Pipeline]
        CheckTrigger[1. Check Recommendation Trigger]
        RouteDecision{Trigger Valid?}
        ReuseCache[Reuse Cached Recommendations]
        CollectCtx[2. Collect User Context]
        AnalyzeBeh[3. Analyze Behavioral Profile]
        SemanticRet[4. Semantic Retrieval]
        BuildCand[5. Build Product Candidates]
        HybridRank[6. 3-Tier Hybrid Ranking]
        GenerateLLM[7. LLM Rationale Generation]
        
        CheckTrigger --> RouteDecision
        RouteDecision -->|No Change| ReuseCache
        RouteDecision -->|New Events| CollectCtx
        CollectCtx --> AnalyzeBeh
        AnalyzeBeh --> SemanticRet
        SemanticRet --> BuildCand
        BuildCand --> HybridRank
        HybridRank --> GenerateLLM
    end
    
    RecAgent --> CheckTrigger
    SemanticRet --> |Query User Vector| QdrantService[Qdrant Vector DB]
    QdrantService --> |Cosine Similarity Search| SentenceTransformer[SentenceTransformers all-MiniLM-L6-v2]
    GenerateLLM --> |Generate JSON Rationale| MeshLLM[Mesh API / LLM tencent/hy3]
    GenerateLLM --> |Persist Recs| DB
```

---

## ✨ Core Features & Technical Highlights

### 1. Real-Time Behavioral Ingestion & Event Tracking
* An in depth report in feature_report_and_recommendation_system.md
* Captures high-granularity micro-interactions:
  * `PRODUCT_VIEW`: Product page visits.
  * `SEARCH`: User search queries with term extraction.
  * `FILTER`: User filter selections (difficulty, language, tags).
  * `TIME_SPENT`: Dwell time in seconds spent viewing content.
  * `SCROLL_DEPTH`: Page scroll percentage (0–100%).
* Asynchronous event logging with session and user isolation.

### 2. Product Interaction Memory & Exponential Recency Decay
* Aggregates raw events per `(user_id, product_id)` pair.
* Calculates interaction intensity based on logarithmic view counts, dwell time, scroll depth, and search frequencies.
* Applies exponential time decay `Recency = e^(-0.10 * age_days)` to prioritize recent user interest over old activity.

### 3. Automated Behavior Profiling & Purchase Intent Modeling
* Dynamically constructs user preference models across categories, difficulty levels, and languages.
* Computes mathematical purchase intent scores ($0.0 \to 1.0$) based on engagement thresholds (e.g. dwell time $\ge 60\text{s}$, scroll depth $\ge 75\%$).
* Normalizes preference distributions to prevent popularity bias.

### 4. High-Dimensional Vector Search (Qdrant Vector DB)
* Vectorizes product titles, descriptions, categories, difficulty, language, skills, and tags using `SentenceTransformers` (`all-MiniLM-L6-v2`, 384 dimensions).
* Dynamically synthesizes a natural language User Preference Text from top interactions and preferences to build an on-the-fly User Vector Embedding.
* Performs sub-millisecond vector similarity search in Qdrant.

### 5. 3-Tier Hybrid Ranking Engine
* Integrates three distinct scoring signals:
  $$\text{Final Score} = 0.50 \times \text{Behavioral Score} + 0.35 \times \text{Semantic Score} + 0.15 \times \text{Preference Score}$$
* **Tier 1**: Direct historical interaction with pre-computed final scores.
* **Tier 2**: On-the-fly metric computation from raw event data if pre-calculated metrics are pending.
* **Tier 3 (Cold-Start)**: 50% category engagement fallback for products the user has never directly interacted with.

### 6. Stateful LangGraph Agentic Pipeline (`recommendation_agent_v2`)
* Orchestrates recommendation workflow as a stateful graph:
  1. `check_recommendation_trigger`: Evaluates whether fresh event data warrants recalculation or if cached recommendations can be safely served.
  2. `collect_context`: Gathers behavior profiles, historical interactions, and top products.
  3. `analyze_behavior`: Synthesizes behavioral metrics for downstream consumption.
  4. `semantic_retrieval`: Embeds user preference text and queries Qdrant vector storage.
  5. `build_candidates`: Joins Qdrant payloads with relational product records in PostgreSQL.
  6. `hybrid_rank`: Applies 3-tier hybrid scoring.
  7. `generate_ai_recommendation`: Passes ranked candidates to LLM for reasoning generation.

### 7. LLM Reasoning & Rationale Generation
* Interfaces with Mesh API (`tencent/hy3` model) to create personalized text recommendations.
* Strict JSON structure enforcement (`product_id`, `title`, `reason`, `confidence`).
* Automatically matches product IDs to prevent hallucinated recommendations.

### 8. Full-Stack Web App & Admin Dashboard
* Built with FastAPI, Jinja2 Templates, HTML5, and custom Vanilla CSS.
* Complete authentication flow (JWT Access/Refresh tokens, Bcrypt password hashing).
* Admin portal for re-indexing products into Qdrant, triggering profile recalculations, and inspecting live interactions.

---

## 🔬 Recommendation System: Mathematical Deep Dive

The SmartReco recommendation engine operates on a multi-stage pipeline combining mathematical heuristic modeling and vector embedding similarity.

### 1. Product Interaction Score Calculation
For any specific user and product, raw interaction metrics are normalized and weighted:

`ViewScore = min(ln(1 + view_count) / ln(1 + 20), 1.0)`

`TimeScore = min(total_time_spent / 300, 1.0)`

`ScrollScore = min(max_scroll_depth / 100, 1.0)`

`SearchScore = min(search_count / 5, 1.0)`

`InteractionScore = 0.30 * ViewScore + 0.30 * TimeScore + 0.25 * ScrollScore + 0.15 * SearchScore`

### 2. Recency Decay Function
Interactions decay exponentially based on elapsed days since the last interaction:

`RecencyScore = e^(-0.10 * age_days)`

`Final Behavioral Score (Interacted) = InteractionScore * RecencyScore`

### 3. Purchase Intent Modeling
Purchase intent represents the user's likelihood to enroll/buy:

`RawIntent = sum(Weight(event_type) * e^(-0.10 * age_days))`

`PurchaseIntent = 1 - e^(-RawIntent)`

Where weights are:
* `PRODUCT_VIEW`: 0.05
* `SEARCH`: 0.03
* `FILTER`: 0.04
* `TIME_SPENT` ($\ge 60\text{s}$): 0.10
* `SCROLL_DEPTH` ($\ge 75\%$): 0.08

### 4. Preference Match Score
Measures catalog alignment with user category and difficulty affinities:
`PreferenceScore = 0.60 * CategoryScore(product.category) + 0.40 * DifficultyScore(product.difficulty)`

### 5. Final Hybrid Ranking Equation
`HybridScore = 0.50 * S_behavioral + 0.35 * S_semantic + 0.15 * S_preference`

---

## 🗄️ Database Schemas

SmartReco uses **PostgreSQL** for relational state and **Qdrant** for vector storage.

### Key Relational Tables (`PostgreSQL`)

* **`users`**: User identity, email, hashed password, role (`admin`/`user`).
* **`products`**: Course catalog (title, description, category, difficulty, language, duration, price, instructor, skills, tags, embedding status).
* **`events`**: Event log (`user_id`, `session_id`, `event_type`, `product_id`, `category`, `search_query`, `event_metadata`, `created_at`).
* **`product_interactions`**: Per-user product aggregated metrics (`view_count`, `total_time_spent`, `max_scroll_depth`, `search_count`, `interaction_score`, `recency_score`, `final_score`, `last_interacted_at`).
* **`behavior_profiles`**: User profile aggregates (`category_scores`, `difficulty_scores`, `language_scores`, `search_frequency`, `average_time_spent`, `average_scroll_depth`, `purchase_intent`, `total_events`, `last_updated`).
* **`recommendations`**: Generated recommendation history (`user_id`, `product_id`, `rank`, `behavioral_score`, `semantic_score`, `preference_score`, `final_score`, `created_at`).

### Vector Storage Collection (`Qdrant`)

* **Collection Name**: `smartreco_products`
* **Vector Dimensions**: `384` (Cosine Distance)
* **Payload Fields**: `product_id`, `title`, `category`, `difficulty`, `language`, `skills`, `tags`

---

## 🌐 API Endpoint Reference

### Authentication (`/auth`)
* `POST /auth/register`: Register new user account.
* `POST /auth/login`: Authenticate and receive session JWT token.
* `GET /auth/me`: Fetch current authenticated user details.
* `GET /auth/logout`: End session and clear token.

### Products (`/products`)
* `GET /products`: List catalog products with pagination and category/difficulty filtering.
* `GET /products/{product_id}`: View product details.
* `POST /products`: Create new product (Admin only).
* `POST /products/index-qdrant`: Batch index all products into Qdrant vector database.

### Events (`/events`)
* `POST /events`: Ingest raw behavioral event (`PRODUCT_VIEW`, `SEARCH`, `FILTER`, `TIME_SPENT`, `SCROLL_DEPTH`).

### Recommendations (`/recommendations`)
* `GET /recommendations`: Get top personalized recommendations for current logged-in user via LangGraph agent.
* `POST /recommendations/generate`: Force recalculation of recommendations.

### Admin Dashboard (`/admin`)
* `GET /admin/dashboard`: Main analytics view.
* `GET /admin/users`: User management list.
* `POST /admin/rebuild-profiles`: Trigger bulk behavior profile rebuilds from event logs.

---

## ⚙️ Installation & Setup Guide

### Prerequisites
* Python 3.10+
* PostgreSQL DB
* Qdrant Vector DB (running locally or via Docker)

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/Aditi3812/smartreco.git
cd smartreco
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables (`.env`)
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smartreco
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

QDRANT_HOST=localhost
QDRANT_PORT=6333

MESH_API_KEY=your_mesh_api_key
```

### 3. Start Qdrant Docker Container
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Seed Initial Data & Vectorize Catalog
```bash
python tests/seed_products.py
python create_qdrant_collection.py
```

### 6. Launch FastAPI Application
```bash
uvicorn app.main:app --reload
```
Navigate to `http://127.0.0.1:8000` in your web browser.

---

## 🧪 Testing Suite

Run all automated unit and integration tests with `pytest`:
```bash
pytest tests/
```

Individual component tests:
* `test_hybrid_ranking.py`: Verifies hybrid mathematical scoring & tier fallbacks.
* `test_qdrant_search.py`: Validates vector insertion and similarity retrieval.
* `test_agent_v2.py`: Tests full LangGraph agent workflow execution.
* `test_event_service.py`: Tests real-time event tracking and behavior profile updates.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
