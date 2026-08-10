from app.database.database import SessionLocal
from app.schemas.product import ProductCreate
from app.services.product_service import product_service


products = [

    # ============================================================
    # AI / MACHINE LEARNING
    # ============================================================

    {
        "title": "Generative AI Masterclass",
        "description": "Learn generative AI, foundation models, prompt engineering, LLM applications, and modern AI workflows from fundamentals to practical projects.",
        "category": "AI",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 40,
        "price": 1299,
        "instructor": "Dr. Arjun Mehta",
        "skills": "Python,Generative AI,LLM,Prompt Engineering",
        "tags": "AI,GENAI,LLM,Generative AI",
    },

    {
        "title": "Large Language Model Engineering",
        "description": "Build production-ready applications with large language models, embeddings, vector databases, prompting, evaluation, and inference pipelines.",
        "category": "AI",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 45,
        "price": 1499,
        "instructor": "Neha Sharma",
        "skills": "Python,LLM,Transformers,Embeddings",
        "tags": "AI,LLM,NLP,Generative AI",
    },

    {
        "title": "Retrieval Augmented Generation with RAG",
        "description": "Learn how to build RAG systems using embeddings, vector databases, document retrieval, reranking, and LLM generation.",
        "category": "AI",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 32,
        "price": 1199,
        "instructor": "Rahul Verma",
        "skills": "Python,RAG,Embeddings,Qdrant,LLM",
        "tags": "AI,RAG,VECTOR DATABASE,LLM",
    },

    {
        "title": "Computer Vision with Deep Learning",
        "description": "Build computer vision applications using convolutional neural networks, image classification, object detection, and deep learning.",
        "category": "AI",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 38,
        "price": 1399,
        "instructor": "Priya Nair",
        "skills": "Python,Computer Vision,CNN,Deep Learning",
        "tags": "AI,CV,DEEP LEARNING,IMAGE PROCESSING",
    },

    {
        "title": "Natural Language Processing Bootcamp",
        "description": "Learn NLP fundamentals including text processing, embeddings, transformers, sentiment analysis, classification, and language models.",
        "category": "AI",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 35,
        "price": 1099,
        "instructor": "Ananya Rao",
        "skills": "Python,NLP,Transformers,Machine Learning",
        "tags": "AI,NLP,TEXT,LANGUAGE MODELS",
    },

    # ============================================================
    # DATA SCIENCE / ML
    # ============================================================

    {
        "title": "Python for Data Science",
        "description": "Master Python for data analysis using NumPy, Pandas, Matplotlib, data cleaning, visualization, and exploratory data analysis.",
        "category": "Data Science",
        "difficulty": "Beginner",
        "language": "English",
        "duration": 28,
        "price": 799,
        "instructor": "Karan Singh",
        "skills": "Python,NumPy,Pandas,Matplotlib",
        "tags": "DATA SCIENCE,PYTHON,ANALYTICS",
    },

    {
        "title": "Machine Learning from Scratch",
        "description": "Understand machine learning algorithms from fundamentals including regression, classification, clustering, feature engineering, and model evaluation.",
        "category": "Data Science",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 42,
        "price": 1199,
        "instructor": "Vikram Kapoor",
        "skills": "Python,Scikit-learn,Regression,Classification",
        "tags": "ML,MACHINE LEARNING,DATA SCIENCE",
    },

    {
        "title": "Deep Learning with PyTorch",
        "description": "Learn neural networks, backpropagation, optimization, CNNs, RNNs, and practical deep learning using PyTorch.",
        "category": "Data Science",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 44,
        "price": 1399,
        "instructor": "Riya Malhotra",
        "skills": "Python,PyTorch,Neural Networks,CNN",
        "tags": "DEEP LEARNING,PYTORCH,AI,NEURAL NETWORKS",
    },

    {
        "title": "Statistics for Machine Learning",
        "description": "Learn probability, distributions, hypothesis testing, correlation, regression, and statistical concepts required for machine learning.",
        "category": "Data Science",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 24,
        "price": 699,
        "instructor": "Dr. Sameer Gupta",
        "skills": "Statistics,Probability,Python,Mathematics",
        "tags": "STATISTICS,ML,MATH,DATA SCIENCE",
    },

    # ============================================================
    # PROGRAMMING
    # ============================================================

    {
        "title": "Advanced Python Programming",
        "description": "Master Python programming with object oriented programming, decorators, generators, concurrency, APIs, testing, and clean architecture.",
        "category": "Programming",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 36,
        "price": 899,
        "instructor": "Aman Joshi",
        "skills": "Python,OOPS,APIs,Testing",
        "tags": "PYTHON,PROGRAMMING,OOPS,BACKEND",
    },

    {
        "title": "Java Programming Bootcamp",
        "description": "Learn Java programming, object oriented programming, collections, exception handling, multithreading, and application development.",
        "category": "Programming",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 34,
        "price": 899,
        "instructor": "Rohit Das",
        "skills": "Java,OOPS,Collections,Multithreading",
        "tags": "JAVA,PROGRAMMING,OOPS",
    },

    {
        "title": "Data Structures and Algorithms",
        "description": "Master arrays, linked lists, stacks, queues, trees, graphs, sorting, searching, recursion, and algorithmic problem solving.",
        "category": "Programming",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 50,
        "price": 999,
        "instructor": "Aditya Kulkarni",
        "skills": "C++,DSA,Algorithms,Problem Solving",
        "tags": "DSA,ALGORITHMS,CODING,INTERVIEW",
    },

    {
        "title": "C Programming Fundamentals",
        "description": "Learn programming fundamentals using C including variables, loops, functions, pointers, arrays, structures, and memory management.",
        "category": "Programming",
        "difficulty": "Beginner",
        "language": "English",
        "duration": 25,
        "price": 599,
        "instructor": "Manish Shah",
        "skills": "C,Pointers,Programming,Data Structures",
        "tags": "C,PROGRAMMING,BASICS",
    },

    # ============================================================
    # WEB DEVELOPMENT
    # ============================================================

    {
        "title": "Full Stack Web Development",
        "description": "Build complete web applications using HTML, CSS, JavaScript, backend APIs, databases, authentication, and deployment.",
        "category": "Web Development",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 55,
        "price": 1499,
        "instructor": "Siddharth Jain",
        "skills": "HTML,CSS,JavaScript,Python,SQL",
        "tags": "WEB,FULL STACK,JAVASCRIPT,BACKEND",
    },

    {
        "title": "React Frontend Development",
        "description": "Build modern interactive frontend applications using React, components, hooks, state management, routing, and API integration.",
        "category": "Web Development",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 30,
        "price": 999,
        "instructor": "Ishita Sen",
        "skills": "React,JavaScript,HTML,CSS,REST APIs",
        "tags": "REACT,FRONTEND,JAVASCRIPT,WEB",
    },

    {
        "title": "FastAPI Backend Development",
        "description": "Build high performance Python APIs using FastAPI, Pydantic, SQLAlchemy, authentication, databases, and REST architecture.",
        "category": "Web Development",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 32,
        "price": 1099,
        "instructor": "Arnav Bose",
        "skills": "Python,FastAPI,SQLAlchemy,PostgreSQL,REST",
        "tags": "FASTAPI,PYTHON,BACKEND,API",
    },

    # ============================================================
    # CYBERSECURITY
    # ============================================================

    {
        "title": "Ethical Hacking Bootcamp",
        "description": "Learn cybersecurity fundamentals, reconnaissance, vulnerability assessment, penetration testing concepts, and defensive security.",
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 40,
        "price": 1299,
        "instructor": "Vivek Menon",
        "skills": "Linux,Networking,Penetration Testing,Security",
        "tags": "CYBERSECURITY,ETHICAL HACKING,PENTESTING",
    },

    {
        "title": "Network Security Fundamentals",
        "description": "Understand network protocols, firewalls, authentication, encryption, intrusion detection, and modern network security architecture.",
        "category": "Cybersecurity",
        "difficulty": "Beginner",
        "language": "English",
        "duration": 26,
        "price": 799,
        "instructor": "Meera Iyer",
        "skills": "Networking,Linux,Security,Encryption",
        "tags": "NETWORK SECURITY,CYBERSECURITY,NETWORKING",
    },

    # ============================================================
    # CLOUD / DEVOPS
    # ============================================================

    {
        "title": "AWS Cloud Practitioner to Architect",
        "description": "Learn AWS cloud fundamentals, EC2, S3, IAM, networking, databases, serverless services, and cloud architecture.",
        "category": "Cloud",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 40,
        "price": 1399,
        "instructor": "Nikhil Agarwal",
        "skills": "AWS,EC2,S3,IAM,Cloud Architecture",
        "tags": "AWS,CLOUD,DEVOPS,ARCHITECTURE",
    },

    {
        "title": "Docker and Kubernetes",
        "description": "Learn containerization, Docker images, networking, Kubernetes clusters, deployments, services, and production orchestration.",
        "category": "DevOps",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 35,
        "price": 1299,
        "instructor": "Harsh Vardhan",
        "skills": "Docker,Kubernetes,Linux,DevOps",
        "tags": "DOCKER,KUBERNETES,DEVOPS,CLOUD",
    },

    {
        "title": "DevOps Engineering with CI CD",
        "description": "Build automated software delivery pipelines using Git, CI/CD, containers, testing, deployment automation, and cloud infrastructure.",
        "category": "DevOps",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 38,
        "price": 1199,
        "instructor": "Saurabh Verma",
        "skills": "Git,CI/CD,Docker,Jenkins,DevOps",
        "tags": "DEVOPS,CICD,AUTOMATION,CLOUD",
    },

    # ============================================================
    # AR / VR
    # ============================================================

    {
        "title": "Unity Game Development",
        "description": "Learn Unity game development, C# scripting, physics, animations, scenes, UI, and building complete interactive games.",
        "category": "Virtual Reality",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 42,
        "price": 1099,
        "instructor": "Kabir Rao",
        "skills": "Unity,C#,Game Development,3D",
        "tags": "UNITY,GAMES,C#,3D,AR/VR",
    },

    {
        "title": "XR and Virtual Reality Development",
        "description": "Build immersive XR applications using Unity, 3D environments, interaction systems, spatial computing, and VR development concepts.",
        "category": "Virtual Reality",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 45,
        "price": 1399,
        "instructor": "Tanvi Kapoor",
        "skills": "Unity,C#,XR,VR,3D",
        "tags": "XR,VR,AR,UNITY,VIRTUAL REALITY",
    },

    # ============================================================
    # UI / UX
    # ============================================================

    {
        "title": "UI UX Design with Figma",
        "description": "Learn user interface and experience design using Figma, wireframes, prototypes, design systems, usability principles, and user research.",
        "category": "UI/UX",
        "difficulty": "Beginner",
        "language": "English",
        "duration": 27,
        "price": 799,
        "instructor": "Ayesha Khan",
        "skills": "Figma,UI Design,UX Design,Prototyping",
        "tags": "UI,UX,FIGMA,DESIGN,PROTOTYPING",
    },

    {
        "title": "Advanced Product Design",
        "description": "Design complete digital products using research, information architecture, interaction design, design systems, prototyping, and usability testing.",
        "category": "UI/UX",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 32,
        "price": 1099,
        "instructor": "Simran Kaur",
        "skills": "Figma,UX Research,Product Design,Design Systems",
        "tags": "PRODUCT DESIGN,UX,UI,FIGMA",
    },

    # ============================================================
    # ROBOTICS
    # ============================================================

    {
        "title": "ROS Robotics Development",
        "description": "Learn robotics software development using ROS, sensors, nodes, topics, navigation, simulation, and robot control.",
        "category": "Robotics",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 40,
        "price": 1499,
        "instructor": "Dr. Rakesh Patel",
        "skills": "ROS,Python,C++,Robotics,Linux",
        "tags": "ROBOTICS,ROS,AUTOMATION,AI",
    },

    {
        "title": "Arduino Robotics for Beginners",
        "description": "Build practical robotics projects using Arduino, sensors, motors, embedded programming, and basic robotics concepts.",
        "category": "Robotics",
        "difficulty": "Beginner",
        "language": "English",
        "duration": 24,
        "price": 699,
        "instructor": "Yash Tiwari",
        "skills": "Arduino,C++,Sensors,Embedded Systems",
        "tags": "ARDUINO,ROBOTICS,EMBEDDED,IOT",
    },

    # ============================================================
    # BLOCKCHAIN
    # ============================================================

    {
        "title": "Blockchain Development Fundamentals",
        "description": "Understand blockchain architecture, cryptography, distributed ledgers, wallets, transactions, consensus, and decentralized applications.",
        "category": "Blockchain",
        "difficulty": "Intermediate",
        "language": "English",
        "duration": 30,
        "price": 999,
        "instructor": "Dev Malhotra",
        "skills": "Blockchain,Cryptography,Web3,JavaScript",
        "tags": "BLOCKCHAIN,WEB3,CRYPTOGRAPHY",
    },

    {
        "title": "Solidity and Smart Contract Development",
        "description": "Build Ethereum smart contracts using Solidity and learn contract architecture, testing, deployment, and decentralized application development.",
        "category": "Blockchain",
        "difficulty": "Advanced",
        "language": "English",
        "duration": 34,
        "price": 1199,
        "instructor": "Aarav Sethi",
        "skills": "Solidity,Ethereum,Smart Contracts,Web3",
        "tags": "SOLIDITY,ETHEREUM,WEB3,BLOCKCHAIN",
    },

]


db = SessionLocal()

created = 0
skipped = 0

try:

    print("\n" + "=" * 80)
    print("SMARTRECO PRODUCT SEEDING")
    print("=" * 80)

    for product_data in products:

        try:

            product = ProductCreate(
                **product_data
            )

            created_product = (
                product_service.create_product(
                    db,
                    product,
                )
            )

            print(
                f"✓ Created #{created_product.id}: "
                f"{created_product.title}"
            )

            created += 1

        except ValueError as e:

            print(
                f"⚠ Skipped: "
                f"{product_data['title']} "
                f"→ {e}"
            )

            skipped += 1

        except Exception as e:

            print(
                f"✗ Failed: "
                f"{product_data['title']} "
                f"→ {e}"
            )

            skipped += 1

    print("\n" + "=" * 80)
    print(
        f"CREATED: {created} | "
        f"SKIPPED/FAILED: {skipped}"
    )
    print("=" * 80)

finally:

    db.close()