# ============================================================
#  SkillBot — Python Flask Backend
#  Interview & Skills Training Chatbot
#  Covers: Soft Skills | Aptitude | Communication | Technical
#  from real company interview databases
# ============================================================

import json
import random
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ============================================================
#  KNOWLEDGE BASE — Interview Q&A categorized by skill type
#  and company. Includes tips, MCQs, and scenario questions.
# ============================================================

KNOWLEDGE_BASE = {
    "soft_skills": {
        "teamwork": [
            {
                "q": "Tell me about a time you worked effectively within a team.",
                "a": "Focus on your specific role, how you collaborated, resolved disagreements, and achieved the goal together. Use the STAR method: Situation, Task, Action, Result.",
                "companies": ["Google", "Amazon", "TCS", "Infosys", "Wipro"],
                "tip": "Emphasize collaboration, active listening, and shared ownership of results."
            },
            {
                "q": "How do you handle conflicts within a team?",
                "a": "Explain that you approach conflict calmly, seek to understand all perspectives, communicate openly, and aim for win-win solutions. Cite a real example if possible.",
                "companies": ["Microsoft", "Deloitte", "Accenture"],
                "tip": "Show emotional intelligence and maturity. Avoid blaming others."
            },
            {
                "q": "Describe a time you helped a struggling teammate.",
                "a": "Talk about how you noticed the issue, offered support without judgment, and collaborated to find solutions. Show empathy and leadership.",
                "companies": ["Capgemini", "IBM", "HCL"],
                "tip": "Demonstrates initiative, empathy, and team-first mindset."
            }
        ],
        "leadership": [
            {
                "q": "Describe a time you led a project or team.",
                "a": "Describe the context, your leadership approach (collaborative vs. directive), how you motivated the team, managed challenges, and the final outcome.",
                "companies": ["Google", "Amazon", "Microsoft", "Flipkart"],
                "tip": "Leaders adapt their style. Show flexibility and results-orientation."
            },
            {
                "q": "What is your leadership philosophy?",
                "a": "Discuss your belief in servant leadership, leading by example, empowering others, and creating psychological safety in teams.",
                "companies": ["McKinsey", "BCG", "KPMG"],
                "tip": "Be authentic. Interviewers want to see your real values."
            },
            {
                "q": "How do you motivate a demotivated team member?",
                "a": "Talk about understanding the root cause (personal, professional, workload), providing support, setting clear achievable goals, and recognizing their contributions.",
                "companies": ["Infosys", "TCS", "Cognizant"],
                "tip": "Show empathy first, action second."
            }
        ],
        "time_management": [
            {
                "q": "How do you prioritize tasks when you have multiple deadlines?",
                "a": "Describe using tools like Eisenhower Matrix, time-boxing, or sprint planning. Give a specific example of balancing multiple priorities successfully.",
                "companies": ["Amazon", "Uber", "Swiggy", "Zomato"],
                "tip": "Mention specific frameworks: Eat the Frog, Pomodoro, or Kanban boards."
            },
            {
                "q": "Tell me about a time you failed to meet a deadline.",
                "a": "Be honest. Explain the circumstances, what you learned, and how you've improved your time management since then.",
                "companies": ["Wipro", "L&T Infotech"],
                "tip": "Own the failure, show reflection, and demonstrate growth."
            }
        ],
        "adaptability": [
            {
                "q": "Tell me about a time you adapted to a significant change at work.",
                "a": "Describe the change (new technology, restructuring, new role), your initial reaction, how you adapted, and what you achieved.",
                "companies": ["Netflix", "Spotify", "Oracle"],
                "tip": "Show resilience, learning agility, and positive attitude toward change."
            },
            {
                "q": "How do you handle ambiguity in your work?",
                "a": "Explain how you break down ambiguous situations, seek clarity proactively, make data-driven assumptions, and iterate. Give a concrete example.",
                "companies": ["Google", "Amazon", "Atlassian"],
                "tip": "Critical for product and tech roles. Show first-principles thinking."
            }
        ],
        "problem_solving": [
            {
                "q": "Describe a difficult problem you faced and how you solved it.",
                "a": "Use STAR format. Focus on the complexity of the problem, your analytical approach, collaboration with others, and measurable impact of your solution.",
                "companies": ["Google", "Meta", "Apple", "Razorpay"],
                "tip": "Structure is key. Interviewers assess your thought process more than the solution."
            },
            {
                "q": "What is your approach to solving problems you've never encountered before?",
                "a": "Break it down into smaller parts, research existing solutions, consult domain experts, prototype solutions, and iterate based on feedback.",
                "companies": ["Startup interviews", "McKinsey", "Google"],
                "tip": "Show curiosity, first-principles thinking, and comfort with uncertainty."
            }
        ]
    },

    "aptitude": {
        "quantitative": [
            {
                "q": "A train travels at 60 km/h and another at 80 km/h in the opposite direction. If they are 420 km apart, after how many hours do they meet?",
                "a": "Relative speed when moving towards each other = 60 + 80 = 140 km/h\nTime = Distance / Speed = 420 / 140 = 3 hours\n**Answer: 3 hours**",
                "companies": ["TCS", "Wipro", "Infosys", "Capgemini", "Accenture"],
                "tip": "For opposite directions, ADD speeds. For same direction, SUBTRACT speeds."
            },
            {
                "q": "A man buys a product for Rs. 1500 and sells it for Rs. 1800. What is the profit percentage?",
                "a": "Profit = 1800 - 1500 = Rs. 300\nProfit % = (300 / 1500) × 100 = **20%**",
                "companies": ["TCS", "Cognizant", "Hexaware"],
                "tip": "Profit % = (Profit / Cost Price) × 100"
            },
            {
                "q": "If 15 workers can complete a project in 12 days, how many days will 9 workers need for the same project?",
                "a": "Total work = 15 × 12 = 180 worker-days\nDays needed for 9 workers = 180 / 9 = **20 days**",
                "companies": ["Infosys", "TCS", "IBM"],
                "tip": "Use the Work = Men × Days formula. This is inverse proportion."
            },
            {
                "q": "Find the compound interest on Rs. 10,000 at 10% per annum for 2 years.",
                "a": "CI = P × [(1 + r/100)^n - 1]\nCI = 10000 × [(1.1)^2 - 1]\nCI = 10000 × [1.21 - 1]\nCI = 10000 × 0.21 = **Rs. 2100**",
                "companies": ["SBI", "HDFC", "Banking sector"],
                "tip": "Remember: Compound interest grows exponentially unlike simple interest."
            },
            {
                "q": "The average of 5 numbers is 24. If one number is removed, the average becomes 21. What is the removed number?",
                "a": "Sum of 5 numbers = 5 × 24 = 120\nSum of 4 numbers = 4 × 21 = 84\nRemoved number = 120 - 84 = **36**",
                "companies": ["Wipro", "HCL", "Tech Mahindra"],
                "tip": "Always convert averages to sums for calculation."
            },
            {
                "q": "A and B together can complete a work in 12 days. A alone can complete it in 20 days. In how many days can B alone complete the work?",
                "a": "A's 1-day work = 1/20\n(A+B)'s 1-day work = 1/12\nB's 1-day work = 1/12 - 1/20 = 5/60 - 3/60 = 2/60 = 1/30\nB alone completes in **30 days**",
                "companies": ["TCS", "Infosys", "Cognizant"],
                "tip": "Express each person's work rate as a fraction per day."
            }
        ],
        "logical_reasoning": [
            {
                "q": "All roses are flowers. Some flowers fade quickly. Which conclusion is valid?",
                "a": "**Conclusion: Some roses may fade quickly.** (But not all roses definitely fade quickly)\nThis is a valid inference — we cannot conclude all roses fade quickly since the 'some flowers' may or may not include roses.",
                "companies": ["TCS", "Wipro", "Infosys NQT", "Accenture"],
                "tip": "In syllogisms: 'All A are B, some B are C' does NOT mean 'some A are C'."
            },
            {
                "q": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
                "a": "Pattern: 1×2, 2×3, 3×4, 4×5, 5×6, 6×7 = **42**\nDifferences: 4, 6, 8, 10, 12 (arithmetic progression with common difference 2)",
                "companies": ["Wipro", "HCL", "Hexaware"],
                "tip": "Look for patterns: arithmetic, geometric, or products of consecutive numbers."
            },
            {
                "q": "If PENCIL is coded as QFODLM, how is ERASER coded?",
                "a": "Each letter is shifted by +1 position in the alphabet.\nE→F, R→S, A→B, S→T, E→F, R→S\n**Answer: FSBTFS**",
                "companies": ["TCS", "Capgemini", "Mphasis"],
                "tip": "Identify the shift pattern first by checking 2-3 letters."
            },
            {
                "q": "A clock shows 3:15. What is the angle between the minute and hour hand?",
                "a": "Minute hand at 15 min → 90°\nHour hand at 3:15 → 3×30 + 15×0.5 = 90 + 7.5 = 97.5°\nAngle between = 97.5 - 90 = **7.5°**",
                "companies": ["Microsoft", "Amazon", "Goldman Sachs"],
                "tip": "Hour hand formula: (H × 30) + (M × 0.5) degrees from 12 o'clock."
            }
        ],
        "data_interpretation": [
            {
                "q": "How do you approach reading a bar chart to answer comparison questions quickly?",
                "a": "1. Read the title and axes carefully first\n2. Note the scale and units\n3. Identify the highest/lowest bars visually\n4. For percentage questions, calculate relative differences\n5. Cross-verify your answer with a quick estimate",
                "companies": ["TCS NQT", "Accenture", "Wipro TurboHire"],
                "tip": "Practice speed-reading charts. Most DI questions test pattern recognition, not complex math."
            }
        ]
    },

    "communication": {
        "verbal": [
            {
                "q": "How do you communicate a complex technical concept to a non-technical stakeholder?",
                "a": "Use analogies and real-world comparisons. Avoid jargon. Start with the 'why' and 'what' before 'how'. Use visuals if possible. Check for understanding by asking questions.",
                "companies": ["Google", "Microsoft", "Deloitte", "EY"],
                "tip": "The Feynman Technique: If you can't explain it simply, you don't understand it well enough."
            },
            {
                "q": "Describe a situation where your communication skills helped resolve a misunderstanding.",
                "a": "Describe the misunderstanding clearly, explain how you identified it, the steps you took to clarify (email, meeting, written summary), and how it was resolved.",
                "companies": ["Accenture", "Capgemini", "TCS iON"],
                "tip": "Show active listening and clear, concise expression."
            },
            {
                "q": "How do you give feedback to a team member who is underperforming?",
                "a": "Use the SBI Model: Situation-Behavior-Impact. Be specific, objective, and focus on behaviors not personality. Offer support and ask for their perspective. Follow up.",
                "companies": ["Amazon", "Google", "Deloitte", "PwC"],
                "tip": "Feedback is a gift. Deliver it privately, respectfully, and with genuine intent to help."
            },
            {
                "q": "What strategies do you use to improve your communication skills?",
                "a": "Active reading (books like 'Crucial Conversations'), Toastmasters, journaling, recording yourself and reviewing, seeking feedback from mentors, and practicing daily.",
                "companies": ["All companies HR round"],
                "tip": "Show that you're proactively investing in self-improvement."
            }
        ],
        "written": [
            {
                "q": "How do you structure a professional email for an escalation?",
                "a": "**Structure:**\n1. Clear subject line (Issue + Urgency level)\n2. Brief context (1-2 sentences)\n3. The problem with impact\n4. Steps already taken\n5. What you need from them (specific ask)\n6. Timeline\n7. Professional closing",
                "companies": ["Infosys", "IBM", "Cognizant", "TCS"],
                "tip": "BLUF — Bottom Line Up Front. Busy executives read the first paragraph only."
            },
            {
                "q": "What makes a report or presentation effective?",
                "a": "An effective report: Executive summary upfront, data-driven with clear visuals, logical flow (Problem → Analysis → Findings → Recommendations), action-oriented conclusions, and appropriate length for the audience.",
                "companies": ["McKinsey", "BCG", "Bain", "Consulting firms"],
                "tip": "Ask yourself: 'What decision does the reader need to make?' — then structure accordingly."
            }
        ],
        "presentation": [
            {
                "q": "How do you handle nervousness before a big presentation?",
                "a": "Preparation is the best antidote to nervousness. Also use: power posing, deep breathing (4-7-8 technique), visualizing success, reframing nervousness as excitement, and focusing on the audience's needs rather than your performance.",
                "companies": ["All HR rounds", "Consulting case interviews"],
                "tip": "Know your first sentence perfectly. That's when nervousness peaks."
            },
            {
                "q": "How do you handle tough questions from the audience during a presentation?",
                "a": "Listen fully before responding. Repeat/rephrase the question. If you don't know, say 'That's a great question, let me get back to you with the right data.' Never bluff.",
                "companies": ["Amazon", "Google", "Sales roles", "Product Management"],
                "tip": "Pause before answering. It signals confidence, not hesitation."
            }
        ],
        "listening": [
            {
                "q": "What does active listening mean and how do you practice it?",
                "a": "Active listening means being fully present, not planning your response while the other person speaks. Practices: eye contact, nodding, paraphrasing back ('So what I hear you saying is...'), asking clarifying questions, and removing distractions.",
                "companies": ["Customer-facing roles", "HR interviews", "Team leads"],
                "tip": "The biggest communication mistake is listening to reply instead of listening to understand."
            }
        ]
    },

    "technical": {
        "programming": [
            {
                "q": "Explain the difference between a stack and a queue.",
                "a": "**Stack**: LIFO (Last In, First Out). Operations: push (add to top), pop (remove from top). Use cases: function call stacks, undo operations, browser history.\n\n**Queue**: FIFO (First In, First Out). Operations: enqueue (add to rear), dequeue (remove from front). Use cases: task scheduling, print queues, BFS traversal.\n\n```python\n# Stack\nstack = []\nstack.append(1)  # push\nstack.pop()      # pop\n\n# Queue\nfrom collections import deque\nqueue = deque()\nqueue.append(1)   # enqueue\nqueue.popleft()   # dequeue\n```",
                "companies": ["Google", "Amazon", "Microsoft", "Flipkart", "Paytm"],
                "tip": "Use deque for O(1) queue operations. List pop(0) is O(n)."
            },
            {
                "q": "What is the difference between == and === (in JavaScript) or == and 'is' in Python?",
                "a": "**Python:**\n- `==` checks VALUE equality\n- `is` checks IDENTITY (same memory address)\n\n```python\na = [1, 2, 3]\nb = [1, 2, 3]\na == b  # True (same values)\na is b  # False (different objects)\n```\n\n**JavaScript:**\n- `==` does type coercion (loose equality)\n- `===` checks value AND type (strict equality)\n\n```js\n'1' == 1   // True (type coercion)\n'1' === 1  // False (different types)\n```",
                "companies": ["Infosys", "Wipro", "TCS", "Cognizant", "HCL"],
                "tip": "Always use `===` in JavaScript and `is` only for None/True/False checks in Python."
            },
            {
                "q": "Explain Object-Oriented Programming (OOP) with its 4 pillars.",
                "a": "**4 Pillars of OOP:**\n\n1. **Encapsulation**: Bundling data and methods that operate on that data within a class. Controls access via private/public modifiers.\n\n2. **Inheritance**: A class (child) inherits properties and behaviors from another class (parent). Promotes code reuse.\n\n3. **Polymorphism**: Same interface, different implementations. Method overriding and method overloading.\n\n4. **Abstraction**: Hiding complex implementation details, showing only what's necessary through abstract classes/interfaces.\n\n```python\nclass Animal:  # Abstraction\n    def sound(self):  # Polymorphism\n        pass\n\nclass Dog(Animal):  # Inheritance\n    def sound(self):\n        return 'Woof'\n```",
                "companies": ["TCS", "Infosys", "Wipro", "IBM", "Capgemini", "All tech companies"],
                "tip": "Always explain with a real-world example like Animal/Dog or Shape/Circle."
            },
            {
                "q": "What is a REST API and what are its key principles?",
                "a": "**REST** = Representational State Transfer — an architectural style for distributed systems.\n\n**Key Principles:**\n1. **Stateless**: Each request contains all information needed\n2. **Client-Server**: Separation of concerns\n3. **Cacheable**: Responses can be cached\n4. **Uniform Interface**: Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)\n5. **Layered System**: Client doesn't know if it's directly connected to the server\n\n**HTTP Methods:**\n- GET: Read data\n- POST: Create new resource\n- PUT/PATCH: Update resource\n- DELETE: Remove resource",
                "companies": ["All Backend roles", "Infosys", "TCS Digital", "Accenture"],
                "tip": "REST is an architectural STYLE, not a protocol. HTTP is just the most common transport."
            },
            {
                "q": "What is the difference between SQL and NoSQL databases?",
                "a": "**SQL (Relational):**\n- Tables with fixed schema\n- ACID compliant\n- Vertical scaling\n- Use when: data is structured, relationships matter\n- Examples: MySQL, PostgreSQL, Oracle\n\n**NoSQL:**\n- Flexible schema (JSON, documents, key-value, graph)\n- BASE compliant (eventually consistent)\n- Horizontal scaling\n- Use when: high velocity, unstructured/semi-structured data\n- Examples: MongoDB, Redis, Cassandra, DynamoDB\n\n**Rule of thumb:** Use SQL for structured, relational data. Use NoSQL for scale and flexibility.",
                "companies": ["Amazon", "Google", "Flipkart", "Swiggy", "All data roles"],
                "tip": "Know when to use which. Saying 'it depends' and explaining WHY scores well."
            },
            {
                "q": "Explain time complexity with examples.",
                "a": "Time complexity measures how an algorithm's runtime grows with input size.\n\n**Common Complexities (best to worst):**\n- O(1): Constant — Array index access\n- O(log n): Logarithmic — Binary search\n- O(n): Linear — Linear search through array\n- O(n log n): — Merge sort, Heap sort\n- O(n²): Quadratic — Bubble sort, Nested loops\n- O(2ⁿ): Exponential — Recursive Fibonacci without memoization\n\n```python\ndef binary_search(arr, target):  # O(log n)\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1\n```",
                "companies": ["Google", "Amazon", "Microsoft", "Goldman Sachs", "Morgan Stanley"],
                "tip": "For every algorithm you write, always state its time AND space complexity."
            },
            {
                "q": "What is the difference between a process and a thread?",
                "a": "**Process:**\n- Independent program in execution\n- Own memory space (heap, stack, code segment)\n- Heavyweight, slower context switch\n- Processes communicate via IPC (pipes, sockets, shared memory)\n\n**Thread:**\n- Lightweight unit within a process\n- Shares memory space with parent process\n- Faster context switch\n- Communication easier but needs synchronization (locks, semaphores)\n\n**In Python:**\n- Due to the GIL (Global Interpreter Lock), threads cannot truly run in parallel for CPU-bound tasks\n- Use `multiprocessing` for CPU-bound, `threading` for I/O-bound",
                "companies": ["Google", "Microsoft", "Amazon", "Systems software roles"],
                "tip": "Always mention the Python GIL if interviewing for Python roles."
            }
        ],
        "databases": [
            {
                "q": "What is database normalization and what are the normal forms?",
                "a": "**Normalization** reduces redundancy and improves data integrity.\n\n**Normal Forms:**\n- **1NF**: Atomic values, no repeating groups\n- **2NF**: 1NF + No partial dependencies (all non-key attributes depend on FULL primary key)\n- **3NF**: 2NF + No transitive dependencies\n- **BCNF**: Stricter version of 3NF\n\n**Denormalization**: Sometimes done intentionally for read performance (data warehouses, OLAP).",
                "companies": ["All database roles", "TCS", "Infosys", "Oracle"],
                "tip": "Most production databases go up to 3NF. BCNF is academic territory."
            },
            {
                "q": "What is an index in a database and when should you use one?",
                "a": "An **index** is a data structure (usually B-tree or Hash) that speeds up read queries at the cost of slower writes and more storage.\n\n**When to use:**\n- Columns frequently used in WHERE, JOIN, or ORDER BY\n- High cardinality columns (many unique values)\n- Foreign key columns\n\n**When NOT to use:**\n- Small tables (full scan is faster)\n- Columns with very low cardinality (like boolean)\n- Tables with heavy write operations",
                "companies": ["Amazon", "Flipkart", "All data engineering roles"],
                "tip": "Too many indexes slow down writes. The sweet spot is 3-5 indexes per table."
            }
        ],
        "system_design": [
            {
                "q": "How would you design a URL shortener like bit.ly?",
                "a": "**Requirements Clarification:**\n- 100M URLs/day write, 1B reads/day\n- URLs valid for 5 years\n\n**Core Design:**\n1. **API**: POST /shorten (returns short URL), GET /{shortCode} (302 redirect)\n2. **Short Code**: 7-character base62 encoding (62^7 = 3.5 trillion unique URLs)\n3. **Database**: \n   - Write path: MySQL/Postgres (shortCode → longURL)\n   - Cache Layer: Redis (top 20% URLs cover 80% traffic)\n4. **Scalability**: Load balancer → App servers → Sharded DB\n5. **Analytics**: Kafka for click events → Spark → Data warehouse",
                "companies": ["Amazon", "Google", "Flipkart", "Razorpay", "Senior Dev interviews"],
                "tip": "Always clarify scale requirements before designing. Functional reqs → Non-functional reqs → System components."
            },
            {
                "q": "What is the difference between horizontal and vertical scaling?",
                "a": "**Vertical Scaling (Scale Up):**\n- Add more power to existing machines (CPU, RAM, SSD)\n- Simpler, no code changes needed\n- Limit: single machine capacity + single point of failure\n- Cost grows exponentially\n\n**Horizontal Scaling (Scale Out):**\n- Add more machines to the pool\n- Requires load balancing, distributed architecture\n- Theoretically unlimited\n- Industry standard for web services\n\n**When to use Vertical**: Databases initially, when simplicity matters\n**When to use Horizontal**: Stateless services, web servers, microservices",
                "companies": ["All system design rounds", "AWS/Azure/GCP roles"],
                "tip": "Design for horizontal scaling from the start but start with vertical — 'Scale when you need to.'"
            }
        ],
        "data_science": [
            {
                "q": "What is overfitting and how do you prevent it?",
                "a": "**Overfitting**: Model learns training data TOO well, capturing noise and failing to generalize to new data. (Low train error, high test error)\n\n**Prevention Methods:**\n1. **More training data**: Bigger dataset helps generalization\n2. **Cross-validation**: K-fold CV to validate on unseen splits\n3. **Regularization**: L1 (Lasso), L2 (Ridge) penalize model complexity\n4. **Dropout**: Randomly disable neurons during neural network training\n5. **Early stopping**: Stop training when validation loss starts increasing\n6. **Feature selection**: Remove irrelevant features\n7. **Ensemble methods**: Random Forest, Bagging reduce variance",
                "companies": ["Data Science roles", "ML roles", "Amazon", "Google AI", "Flipkart DS"],
                "tip": "The bias-variance tradeoff: Underfitting = high bias. Overfitting = high variance. Aim for the sweet spot."
            }
        ],
        "network": [
            {
                "q": "What happens when you type 'google.com' in a browser and press Enter?",
                "a": "**Step-by-step:**\n1. **DNS Resolution**: Browser → OS cache → DNS resolver → Root DNS → TLD DNS → Authoritative DNS → IP address\n2. **TCP Connection**: 3-way handshake (SYN → SYN-ACK → ACK)\n3. **TLS Handshake** (for HTTPS): Certificate exchange, session key generation\n4. **HTTP Request**: Browser sends GET request with headers\n5. **Server Processing**: Web server → App server → Database (if needed)\n6. **HTTP Response**: HTML, CSS, JS files sent back\n7. **Rendering**: DOM construction, CSSOM, JavaScript execution, layout, paint",
                "companies": ["Google", "Amazon", "Microsoft", "Cloudflare", "All full-stack roles"],
                "tip": "This is one of the most popular interview questions globally. Know it cold."
            }
        ]
    }
}

# Company-specific interview questions database
COMPANY_QUESTIONS = {
    "google": {
        "focus": ["Algorithms", "Data Structures", "System Design", "Behavioral (Googliness)", "Leadership"],
        "tips": [
            "Google uses a structured hiring process with 4-6 rounds",
            "Use STAR method for behavioral questions",
            "Coding questions are algorithm-heavy — practice LeetCode hard",
            "System design asks: 'Design Google Search' level questions",
            "Show passion for technology and learning"
        ],
        "sample_questions": [
            "Find the shortest path in a weighted graph",
            "Design Google Maps",
            "Tell me about a time you disagreed with your manager",
            "How would you handle working on a project with no clear requirements?"
        ]
    },
    "amazon": {
        "focus": ["Leadership Principles (14)", "Coding", "System Design", "Bar Raiser"],
        "tips": [
            "Know all 14 Leadership Principles inside out",
            "Every behavioral question maps to an LP — prepare 2 stories per LP",
            "Amazon's bar raiser is an independent interviewer who focuses on culture",
            "System design: Focus on scalability, reliability, and cost",
            "Use STAR format religiously"
        ],
        "sample_questions": [
            "Tell me about a time you took ownership of a problem",
            "Describe a time you had to deliver results with incomplete information",
            "Design Amazon's order management system",
            "Implement LRU Cache"
        ]
    },
    "tcs": {
        "focus": ["Aptitude", "Verbal Ability", "Coding (easy level)", "HR Interview"],
        "tips": [
            "TCS NQT has 4 sections: Verbal, Aptitude, Programming Logic, Coding",
            "Verbal section is scoring — focus on comprehension and grammar",
            "Coding section is beginner-friendly — know basic loops and arrays",
            "HR interview focuses on communication, adaptability, and culture fit",
            "TCS has service-based role focus — emphasize teamwork and learning agility"
        ],
        "sample_questions": [
            "Write a program to find the factorial of a number",
            "Why do you want to join TCS?",
            "Aptitude: Time and Work, Profit and Loss, Series completion",
            "Verbal: Reading comprehension, Sentence correction"
        ]
    },
    "infosys": {
        "focus": ["Aptitude (InfyTQ platform)", "Pseudocode", "Verbal Ability", "HR", "Technical"],
        "tips": [
            "InfyTQ test: Quantitative ability and logical reasoning are key",
            "Pseudocode section tests algorithmic thinking, not syntax",
            "Technical round focuses on DBMS, OS, Networking, OOP",
            "HR round: Why Infosys, career goals, strengths/weaknesses",
            "Strong campus hiring — CGPA above 6.5 is typically required"
        ],
        "sample_questions": [
            "Write pseudocode for bubble sort",
            "What is normalization in DBMS?",
            "Explain OOPS concepts",
            "Where do you see yourself in 5 years?"
        ]
    },
    "wipro": {
        "focus": ["NLTH (National Level Talent Hunt)", "Aptitude", "Verbal", "Coding", "Technical HR"],
        "tips": [
            "NLTH Online test has Aptitude, Writing, and Coding sections",
            "Writing section: Essay writing is unique to Wipro — practice formal writing",
            "Coding: 2 questions, medium difficulty",
            "Technical HR: Focus on DSA fundamentals and projects",
            "Show interest in cloud and digital transformation (Wipro's focus areas)"
        ],
        "sample_questions": [
            "Write an essay on 'Impact of AI on Jobs' (200 words)",
            "Implement binary search",
            "Explain the OSI model",
            "Describe your best project in detail"
        ]
    },
    "microsoft": {
        "focus": ["Coding (medium-hard)", "Problem Solving", "Behavioral (Growth Mindset)", "Design"],
        "tips": [
            "Microsoft values 'Growth Mindset' — show how you learn from failure",
            "Coding: Focus on arrays, strings, trees, graphs",
            "Think out loud during coding rounds",
            "System design: Emphasize scalability and reliability",
            "Team matching matters at Microsoft — express genuine interest in specific teams"
        ],
        "sample_questions": [
            "Reverse a linked list",
            "Design a video conferencing system like Teams",
            "Tell me about a time you had to learn something new quickly",
            "Implement a cache with expiry"
        ]
    },
    "accenture": {
        "focus": ["Cognitive Assessment", "Technical Assessment", "Communication Round", "HR"],
        "tips": [
            "Accenture hiring: Cognitive + technical assessment online first",
            "Communication round is a video interview — speak clearly and confidently",
            "Technical: Basic programming, SQL, and OOP concepts",
            "Culture: Innovation, diversity, sustainability are core values",
            "Show client-centric thinking and teamwork ability"
        ],
        "sample_questions": [
            "What are the pillars of OOP?",
            "Write a SQL query to find the second highest salary",
            "Why do you want to join Accenture?",
            "How would you handle a difficult client?"
        ]
    },
    "cognizant": {
        "focus": ["Aptitude", "Verbal", "Coding", "Technical Interview", "HR"],
        "tips": [
            "GenC (Graduate Engineering) program: Focus on aptitude and basics",
            "Cognizant values adaptability and continuous learning",
            "Technical: Core CS subjects, data structures, and a mini-project",
            "Code Gladiators and Hackathons strengthen your profile",
            "Strong emphasis on digital skills: Cloud, AI, DevOps"
        ],
        "sample_questions": [
            "Find duplicates in an array",
            "What is the difference between TCP and UDP?",
            "Describe a technical challenge you overcame",
            "What are ACID properties in databases?"
        ]
    }
}

# Greeting patterns
GREETINGS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste", "hola"]

# ============================================================
#  RESPONSE ENGINE
# ============================================================

def find_best_match(query: str) -> dict:
    """Core intent detection and response generation."""
    query_lower = query.lower().strip()
    
    # 1. Greeting detection
    if any(g in query_lower for g in GREETINGS):
        return {
            "type": "greeting",
            "content": "Hello! 👋 I'm **SkillBot**, your personal interview preparation assistant!\n\nI can help you with:\n\n🧠 **Aptitude Skills** — Quantitative, Logical Reasoning, Data Interpretation\n💬 **Communication Skills** — Verbal, Written, Presentation, Active Listening\n🤝 **Soft Skills** — Leadership, Teamwork, Time Management, Adaptability\n💻 **Technical Skills** — Programming, DSA, System Design, Databases, Cloud\n🏢 **Company-wise Questions** — Google, Amazon, TCS, Infosys, Wipro, Microsoft & more\n\nTry asking:\n- *'Show me TCS interview questions'*\n- *'What is teamwork in soft skills?'*\n- *'Binary search time complexity'*\n- *'Communication skills tips'*",
            "follow_up": ["Show aptitude questions", "Technical skills", "Communication tips", "Tell me about TCS"]
        }
    
    # 2. Help command
    if any(word in query_lower for word in ["help", "what can you do", "how to use", "guide"]):
        return {
            "type": "help",
            "content": "## 🎯 SkillBot — What I Can Help You With\n\n**1. 🧠 Aptitude Skills**\n- Quantitative Problems (Time-Speed, Profit-Loss, Ratios, Percentages)\n- Logical Reasoning (Series, Coding-Decoding, Syllogisms)\n- Data Interpretation\n\n**2. 💬 Communication Skills**\n- Professional email writing\n- Presentation tips\n- Active listening techniques\n- Verbal & non-verbal communication\n\n**3. 🤝 Soft Skills**\n- Leadership & Teamwork\n- Time Management\n- Conflict Resolution\n- Problem Solving\n- Adaptability\n\n**4. 💻 Technical Skills**\n- Data Structures & Algorithms\n- OOP, DBMS, OS, Networking\n- System Design\n- Data Science & ML basics\n\n**5. 🏢 Company-wise Prep**\n- Google, Amazon, Microsoft, TCS, Infosys, Wipro, Cognizant, Accenture, and more!\n\n**Sample queries you can try:**\n- `aptitude questions`\n- `how to answer teamwork question`\n- `what is REST API`\n- `Amazon interview tips`\n- `soft skills for freshers`",
            "follow_up": ["Aptitude practice", "Technical questions", "Company-wise questions", "Soft skills"]
        }
    
    # 3. Category-specific searches
    
    # APTITUDE
    if any(word in query_lower for word in ["aptitude", "quantitative", "maths", "math", "reasoning", "logical", "number series", "profit loss", "time speed", "work rate", "percentage"]):
        category = "aptitude"
        if "quantitative" in query_lower or any(w in query_lower for w in ["profit", "speed", "work", "percentage", "train", "average"]):
            sub = "quantitative"
        elif "reasoning" in query_lower or "logical" in query_lower or "series" in query_lower or "syllogism" in query_lower:
            sub = "logical_reasoning"
        else:
            sub = random.choice(list(KNOWLEDGE_BASE["aptitude"].keys()))
        
        questions = KNOWLEDGE_BASE["aptitude"][sub]
        random.shuffle(questions)
        selected = questions[:3]
        
        return {
            "type": "aptitude",
            "topic": sub.replace("_", " ").title(),
            "questions": selected,
            "content": f"## 🧠 Aptitude — {sub.replace('_', ' ').title()}\n\nHere are **practice problems** with full solutions:\n\n---",
            "follow_up": ["More aptitude questions", "Logical reasoning", "Data interpretation", "Tips for aptitude tests"]
        }
    
    # SOFT SKILLS
    if any(word in query_lower for word in ["soft skill", "teamwork", "team work", "leadership", "time management", "adaptability", "problem solv", "interpersonal", "behavioural", "behavioral", "collaboration"]):
        if "team" in query_lower:
            sub = "teamwork"
        elif "leader" in query_lower:
            sub = "leadership"
        elif "time" in query_lower:
            sub = "time_management"
        elif "adapt" in query_lower:
            sub = "adaptability"
        elif "problem" in query_lower:
            sub = "problem_solving"
        else:
            sub = random.choice(list(KNOWLEDGE_BASE["soft_skills"].keys()))
        
        questions = KNOWLEDGE_BASE["soft_skills"][sub]
        
        return {
            "type": "soft_skills",
            "topic": sub.replace("_", " ").title(),
            "questions": questions,
            "content": f"## 🤝 Soft Skills — {sub.replace('_', ' ').title()}\n\nHere are **interview questions** asked by top companies:\n\n---",
            "follow_up": ["Leadership questions", "Teamwork tips", "STAR method explained", "More behavioral questions"]
        }
    
    # COMMUNICATION SKILLS
    if any(word in query_lower for word in ["communication", "email", "presentation", "verbal", "written", "speak", "listening", "active listen", "feedback", "stakeholder"]):
        if "email" in query_lower or "written" in query_lower:
            sub = "written"
        elif "presentation" in query_lower or "public speak" in query_lower:
            sub = "presentation"
        elif "listen" in query_lower:
            sub = "listening"
        else:
            sub = random.choice(list(KNOWLEDGE_BASE["communication"].keys()))
        
        questions = KNOWLEDGE_BASE["communication"][sub]
        
        return {
            "type": "communication",
            "topic": sub.replace("_", " ").title(),
            "questions": questions,
            "content": f"## 💬 Communication Skills — {sub.replace('_', ' ').title()}\n\n---",
            "follow_up": ["Email writing tips", "Presentation skills", "Active listening", "Giving feedback"]
        }
    
    # TECHNICAL
    if any(word in query_lower for word in ["technical", "programming", "coding", "algorithm", "data structure", "stack", "queue", "oop", "object oriented", "api", "rest", "sql", "nosql", "database", "system design", "url shortener", "machine learning", "python", "java", "javascript", "thread", "process", "dns", "http", "tcp", "complexity", "sorting", "binary search", "normalization", "index", "overfitting"]):
        # Sub-category detection
        if any(word in query_lower for word in ["system design", "url shortener", "scale", "distributed", "microservice"]):
            sub = "system_design"
        elif any(word in query_lower for word in ["database", "sql", "nosql", "normalization", "index", "acid"]):
            sub = "databases"
        elif any(word in query_lower for word in ["machine learning", "ml", "ai", "overfitting", "neural", "data science", "model"]):
            sub = "data_science"
        elif any(word in query_lower for word in ["network", "dns", "tcp", "http", "osi", "protocol"]):
            sub = "network"
        else:
            sub = "programming"
        
        questions = KNOWLEDGE_BASE["technical"][sub]
        
        return {
            "type": "technical",
            "topic": sub.replace("_", " ").title(),
            "questions": questions,
            "content": f"## 💻 Technical Skills — {sub.replace('_', ' ').title()}\n\n---",
            "follow_up": ["System design questions", "Database questions", "DSA concepts", "Python interview tips"]
        }
    
    # COMPANY-SPECIFIC
    for company_name, company_data in COMPANY_QUESTIONS.items():
        if company_name in query_lower or company_name.replace("_", " ") in query_lower:
            return {
                "type": "company",
                "company": company_name.upper(),
                "data": company_data,
                "content": f"## 🏢 {company_name.upper()} — Interview Preparation Guide\n\n---",
                "follow_up": [f"More {company_name.upper()} tips", "Technical questions", "HR round prep", "Aptitude practice"]
            }
    
    # STAR METHOD
    if "star" in query_lower or "star method" in query_lower:
        return {
            "type": "info",
            "content": "## ⭐ The STAR Method — Your Secret Weapon for Behavioral Interviews\n\nThe STAR method is a structured approach to answering behavioral interview questions.\n\n---\n\n**S — Situation**\nSet the context. Describe the specific situation or challenge you faced.\n*Example: 'In my final year project, we had 3 members drop out 2 weeks before the deadline...'*\n\n**T — Task**\nExplain your responsibility. What was your specific role?\n*Example: '...and I was the project lead, responsible for re-distributing work and ensuring we still delivered on time.'*\n\n**A — Action**\nDescribe the SPECIFIC actions YOU took. Use 'I' not 'we'.\n*Example: 'I immediately called a team meeting, broke the remaining work into 2-hour sprints, brought in one new volunteer, and personally took on the critical integration module.'*\n\n**R — Result**\nShare the measurable outcome. Quantify wherever possible.\n*Example: 'We delivered the project on time, received an A grade, and the project was selected for the college tech fest.'*\n\n---\n\n**💡 Pro Tips:**\n- Prepare 8-10 STAR stories covering different themes\n- Each story should be reusable across multiple questions\n- Focus on YOUR actions, not the team's\n- Always end with a positive result (even in failure stories, show what you learned)",
            "follow_up": ["Behavioral questions practice", "Leadership STAR story", "Teamwork STAR example", "Conflict resolution example"]
        }
    
    # TIPS for freshers
    if any(word in query_lower for word in ["fresher", "fresher tips", "campus", "placement prep", "interview prep", "how to prepare", "preparation tips"]):
        return {
            "type": "info",
            "content": "## 🎓 Complete Placement Preparation Roadmap for Freshers\n\n---\n\n**Phase 1: Foundation (2-3 months before campus)**\n✅ Master 1 programming language (Python/Java/C++)\n✅ Study Data Structures & Algorithms (Arrays, Linked Lists, Trees, Graphs)\n✅ Complete aptitude basics: Quantitative, Logical Reasoning\n✅ Practice 50+ LeetCode Easy problems\n\n**Phase 2: Interview Prep (1-2 months before)**\n✅ Learn DBMS, OS, CN, OOP fundamentals\n✅ Practice aptitude on platforms: IndiaBix, PrepInsta, GeeksForGeeks\n✅ Solve 20+ LeetCode Medium problems\n✅ Prepare 8-10 STAR stories for behavioral rounds\n✅ Mock interviews with friends\n\n**Phase 3: Company-Specific Prep (2 weeks before)**\n✅ Study the company's products, mission, and recent news\n✅ Solve that company's tagged problems on LeetCode\n✅ Review the company's Leadership Principles / Core Values\n✅ Prepare smart questions to ask the interviewer\n\n**Phase 4: D-Day**\n✅ Sleep well the night before\n✅ Arrive/log in 10 minutes early\n✅ Have your resume, notepad, and pen ready\n✅ Speak your thought process out loud during coding\n✅ Thank the interviewer at the end",
            "follow_up": ["TCS preparation guide", "Infosys tips", "Aptitude practice", "Technical interview prep"]
        }
    
    # HR questions
    if any(word in query_lower for word in ["hr", "tell me about yourself", "weakness", "strength", "where do you see yourself", "why should we hire", "salary", "career goal"]):
        return {
            "type": "info",
            "content": "## 🏢 Top HR Interview Questions & How to Answer Them\n\n---\n\n**1. 'Tell me about yourself'**\nFormula: Present → Past → Future\n*'I am a final year Computer Science student from [College]. I have a strong foundation in Python and have built [project]. Previously, I interned at [company] where I [achievement]. I am now looking for a role where I can [goal aligned to company].'*\n\n**2. 'What is your greatest strength?'**\nPick a strength relevant to the role. Prove it with an example.\n*'My greatest strength is problem-solving. When our college hackathon server crashed during the final hour, I quickly reconfigured the setup and we recovered in 20 minutes.'*\n\n**3. 'What is your greatest weakness?'**\nShow self-awareness + growth mindset.\n*'I tend to overthink before making decisions. I've been working on this by setting time-boxed decision deadlines for myself, and it's helped me become more decisive.'*\n\n**4. 'Why do you want to join [Company]?'**\nResearch → Align → Contribute\n*'I'm impressed by Amazon's Day 1 culture and the scale of problems you solve. As someone who loves building for scale, working here would help me grow and contribute to [specific team/product].'*\n\n**5. 'Where do you see yourself in 5 years?'**\n*'I see myself as a subject matter expert in [domain], having taken on leadership responsibilities and contributed to meaningful products. I want to grow with this company and tackle increasingly complex challenges.'*\n\n**6. 'Do you have any questions for us?'**\nALWAYS ask questions. Good ones:\n- 'What does success look like in this role in the first 6 months?'\n- 'What are the biggest challenges the team is currently facing?'\n- 'How do you support learning and development here?'",
            "follow_up": ["STAR method", "Behavioral questions", "Company-specific tips", "Fresher interview guide"]
        }
    
    # Default: fuzzy keyword search across all categories
    results = []
    query_words = set(query_lower.split())
    
    for category, subcats in KNOWLEDGE_BASE.items():
        for subcat, items in subcats.items():
            for item in items:
                score = 0
                # Check word overlap with question and answer
                item_text = (item["q"] + " " + item["a"]).lower()
                for word in query_words:
                    if len(word) > 3 and word in item_text:
                        score += 1
                if score > 0:
                    results.append((score, category, subcat, item))
    
    if results:
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:3]
        response_items = [r[3] for r in top_results]
        category_name = top_results[0][1].replace("_", " ").title()
        
        return {
            "type": "search_result",
            "content": f"## 🔍 Search Results for: *'{query}'*\n\nFound **{len(results)} matching entries** across all skill categories. Showing top results:\n\n---",
            "questions": response_items,
            "follow_up": ["Aptitude skills", "Communication tips", "Technical questions", "Soft skills"]
        }
    
    # Absolute fallback
    return {
        "type": "fallback",
        "content": f"## 🤔 I couldn't find an exact match for: *'{query}'*\n\nBut I can help you with:\n\n🧠 **Aptitude** → try: *'aptitude questions'*, *'profit loss problem'*, *'number series'*\n💬 **Communication** → try: *'email writing tips'*, *'presentation skills'*, *'verbal communication'*\n🤝 **Soft Skills** → try: *'teamwork question'*, *'leadership example'*, *'STAR method'*\n💻 **Technical** → try: *'what is OOP'*, *'binary search'*, *'system design'*\n🏢 **Companies** → try: *'TCS interview'*, *'Amazon tips'*, *'Google questions'*\n\nType `/help` to see everything I can do!",
        "follow_up": ["Aptitude practice", "Soft skills tips", "Technical interview", "Company guide"]
    }


def format_response(result: dict) -> dict:
    """Convert internal result to API response format."""
    response = {
        "content": result.get("content", ""),
        "type": result.get("type", "info"),
        "follow_up": result.get("follow_up", []),
        "items": []
    }
    
    questions = result.get("questions", [])
    
    if result["type"] == "company":
        data = result.get("data", {})
        company = result.get("company", "")
        content = result["content"]
        content += f"\n\n**🎯 Focus Areas:**\n" + "\n".join([f"- {f}" for f in data.get("focus", [])])
        content += f"\n\n**📋 Sample Interview Questions:**\n" + "\n".join([f"- {q}" for q in data.get("sample_questions", [])])
        content += f"\n\n**💡 Insider Tips:**\n" + "\n".join([f"- {t}" for t in data.get("tips", [])])
        response["content"] = content
        return response
    
    for item in questions:
        response["items"].append({
            "question": item.get("q", ""),
            "answer": item.get("a", ""),
            "companies": item.get("companies", []),
            "tip": item.get("tip", "")
        })
    
    return response


# ============================================================
#  FLASK ROUTES
# ============================================================

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data['message'].strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    result = find_best_match(user_message)
    response = format_response(result)
    
    return jsonify({
        "success": True,
        "response": response
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Return all available categories and sub-categories."""
    categories = {}
    for cat, subcats in KNOWLEDGE_BASE.items():
        categories[cat] = {
            "name": cat.replace("_", " ").title(),
            "subcategories": list(subcats.keys())
        }
    return jsonify({
        "categories": categories,
        "companies": list(COMPANY_QUESTIONS.keys())
    })


@app.route('/api/random-question', methods=['GET'])
def random_question():
    """Return a random interview question from any category."""
    category = random.choice(list(KNOWLEDGE_BASE.keys()))
    subcat = random.choice(list(KNOWLEDGE_BASE[category].keys()))
    question = random.choice(KNOWLEDGE_BASE[category][subcat])
    
    return jsonify({
        "category": category.replace("_", " ").title(),
        "subcategory": subcat.replace("_", " ").title(),
        "question": question
    })


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    print("=" * 60)
    print("  SkillBot Backend starting...")
    print("  URL: http://localhost:5000")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
