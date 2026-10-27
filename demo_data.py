"""Small SYNTHETIC demo sets so anyone can try the app. No real student or applicant data.
Shafaq's own larger synthetic sets (incl. scanned handwriting) are used in the notebook."""

EXAM_BANK = """C1 - Explaining the stage (0-2)
+ 2 marks: gives the age range (about 7-11) AND says children think logically about concrete/real objects AND names at least one key idea (conservation, reversibility, classification, seriation).
+ 1 mark: only one or two of these (e.g. age + "logical", but no concrete objects or key idea).
- 0 marks: describes a different stage (e.g. abstract/hypothetical thinking = formal operational), or only says who Piaget was.
- Common mistake: mixing up concrete operational with formal operational (abstract thinking, adolescence). This earns 0 for C1 even if the answer is long.

C2 - Two classroom applications (0-2, 1 each)
+ 1 mark each: a specific activity using hands-on or real objects (counters, base-ten blocks, sorting leaves, water jugs for conservation, class shop with play money).
- No mark: vague advice ("use activities", "give examples", "use charts because children like colours") with no link to concrete thinking.
- No mark: an activity that fits another theory (e.g. scaffolding/ZPD from Vygotsky) unless it is tied to concrete objects.

C3 - Link to Grade 3 (0-1)
+ 1 mark: says why it suits Grade 3 / age 8-9 children (they learn best with concrete, hands-on materials).
- No mark: Grade 3 only mentioned in passing, or the reason is unrelated to the stage.

General
- Do not reward length or big words. Short, correct answers can earn full marks.
- Ignore spelling and grammar. Weak English with correct ideas earns full credit.
- An answer that only repeats the question earns 0.
- An answer about a different theory (e.g. Vygotsky only) earns 0.

Standard feedback comments
- "Good: you linked the stage to hands-on classroom activities."
- "Add the age range and one key idea such as conservation."
- "Your activities need to use real or concrete objects to fit this stage."
- "Explain why this suits Grade 3 children (age 8-9)."
- "This describes abstract thinking, which belongs to the formal operational stage."
"""

EXAM = {
    "task": ("Course: Child Development (B.Ed)\n"
             "Q1. Explain Piaget's concrete operational stage and give TWO ways a Grade 3 teacher "
             "can use it in the classroom. (5 marks)"),
    "rubric": ("C1. Stage explained correctly - about ages 7 to 11; children think logically about concrete, "
               "real objects; key ideas such as conservation, reversibility or classification. (0-2 marks)\n"
               "C2. Two valid classroom applications that fit this stage, 1 mark each. (0-2 marks)\n"
               "C3. Applications clearly linked to Grade 3 children (age 8-9). (0-1 mark)\n"
               "Total: 5 marks"),
    "bank": EXAM_BANK,
    "documents": [
        {"id": "S01", "label": "strong", "text": "Concrete operational stage is the third stage of Piaget, from about 7 to 11 years. Children can think logically but only about real, concrete things they can see or touch. They understand conservation, for example the water is same even in a tall glass, and reversibility and classification. A Grade 3 teacher can use counters and blocks to teach addition and subtraction so children see it physically. Second, she can do sorting activities, like sorting leaves by shape and size in science. Grade 3 children are 8 years old so hands-on objects suit them."},
        {"id": "S02", "label": "good", "text": "In this stage (7-11 years) child thinks logically about concrete objects. Child understands conservation of number and volume. Teacher can use real objects like beads for maths. Teacher can also do group activities where children classify animals into groups."},
        {"id": "S03", "label": "average", "text": "Piaget said children go through stages. Concrete operational is when child is around 7 to 11. They start to think logically. Teacher should use activities in class and give examples so children learn better."},
        {"id": "S04", "label": "weak English, correct", "text": "this stage child age 7 to 11 year. child can thinking logic but with real thing only, not abstract. he understand if we pour water in thin glass, water is same (conservation). teacher in class 3 give child sticks for counting and making bundle of ten. also teacher make child sort pictures of fruit and vegetable. class 3 child is 8 year so real thing is good for him."},
        {"id": "S05", "label": "trap: long but wrong", "text": "The concrete operational stage is the most advanced stage of cognitive development in which learners engage in hypothetico-deductive reasoning, abstract thought, and metacognitive reflection about hypothetical possibilities. At this stage, typically adolescence and beyond, students can manipulate abstract symbols, consider propositions, and reason scientifically about variables without needing concrete referents. Therefore, a teacher should design debates on abstract moral dilemmas and encourage students to formulate and test hypotheses independently, fostering higher-order critical thinking, metacognition, and twenty-first century skills across the curriculum."},
        {"id": "S06", "label": "trap: copies question", "text": "Piaget's concrete operational stage is a stage and a Grade 3 teacher can use it in the classroom in two ways. The teacher can use it in the classroom. This is the concrete operational stage of Piaget."},
        {"id": "S07", "label": "trap: off-topic", "text": "Vygotsky gave the idea of the Zone of Proximal Development, which is the gap between what a child can do alone and what they can do with help. Teachers can use scaffolding and peer tutoring. A more knowledgeable other helps the child to learn."},
        {"id": "S08", "label": "partial", "text": "Concrete operational stage is 7 to 11 years. Child can understand conservation and reversibility. Teacher can use objects for teaching maths."},
        {"id": "S09", "label": "good", "text": "Age 7-11. Logical thinking begins but it is tied to concrete experiences. Classification and seriation develop, e.g. arranging sticks from shortest to longest. In Grade 3, teacher can use a class shop with play money to teach addition, and use a measuring activity with real water jugs to show conservation of volume. Children of 8-9 learn best with such hands-on work."},
        {"id": "S10", "label": "weak", "text": "Piaget was a Swiss psychologist. He worked on child development and gave four stages. Children learn by doing."},
        {"id": "S11", "label": "average", "text": "In concrete stage children are logical about real things. They can classify. Teacher can make groups and give them objects to sort. Teacher can also take them on a field trip."},
        {"id": "S12", "label": "strong, short", "text": "7-11 yrs; logical thinking about concrete objects; conservation, reversibility, classification. Grade 3 (age 8): (1) base-ten blocks for place value, (2) sorting rocks/leaves by properties in science. Both use hands-on objects which suit this age."},
        {"id": "S13", "label": "average", "text": "This is the stage where children can do conservation. Like if clay ball is made flat it is same clay. Teacher can show this experiment to children in class."},
        {"id": "S14", "label": "partial", "text": "Children from 7 to 11 think logically. Teacher should use pictures and charts and real objects in Grade 3 because children like colourful things."},
    ],
}

RESUME_BANK = """R1 - SQL (0-3)
+ 3: wrote queries in real work or an internship (pulled reports, joins, aggregations).
+ 2: SQL in a substantial project with a clear result.
+ 1: coursework or certificate only.
- 0: SQL only listed as a skill with no evidence.

R2 - Analysis with Excel or Python (0-3)
+ 3: regular real analysis (pivot tables, pandas, cleaning data) at work.
+ 2: a project with a clear question and finding.
+ 1: basic use only.

R3 - Dashboards / visualisation (0-2)
+ 2: built a dashboard or chart report that someone used.
+ 1: made charts in a course project.

R4 - Communication (0-2)
+ 2: presented or wrote up findings for managers or a team.
+ 1: some evidence (class report).

General
- A long skills list without evidence (keyword stuffing) earns little.
- Plain wording with real evidence can earn full marks.
- Ignore name, gender, marital status, age, photo and university name.

Standard feedback comments
- "Strong practical evidence of SQL and reporting."
- "Skills are listed but not shown in any project or job."
- "Add one example of a dashboard or report you built and who used it."
"""

RESUME = {
    "task": ("Job: Junior Data Analyst (entry level), Karachi.\n"
             "Needs: SQL for querying data; Excel or Python for analysis; dashboards (Power BI/Tableau); "
             "clear communication of findings. 0-2 years experience."),
    "rubric": ("R1. SQL - evidence of actually writing queries (projects, work, coursework). (0-3)\n"
               "R2. Analysis with Excel or Python - evidence of real analysis tasks. (0-3)\n"
               "R3. Dashboards / visualisation - built at least one dashboard or report. (0-2)\n"
               "R4. Communication - presented or wrote up findings for others. (0-2)\n"
               "Total: 10 points. Score evidence, not keywords."),
    "bank": RESUME_BANK,
    "documents": [
        {"id": "R01", "label": "strong", "text": "Name: Sana Iqbal\nEmail: sana.iqbal@example.com\nBS Statistics, University of Karachi (2025)\nInternship - Data Intern, FMCG distributor (6 months): wrote SQL queries in PostgreSQL to pull weekly sales by region; built a Power BI dashboard used by the sales manager; cleaned 50k rows in Excel with Power Query.\nProject: Python (pandas) analysis of Karachi rainfall vs. delivery delays; presented results to the operations team.\nSkills: SQL, Excel, Python, Power BI"},
        {"id": "R02", "label": "trap: keyword stuffed", "text": "Name: Bilal Ahmed\nPhone: 0300-1234567\nSKILLS: SQL, MySQL, PostgreSQL, NoSQL, Python, R, Excel, VBA, Power BI, Tableau, Looker, Big Data, Hadoop, Spark, Machine Learning, Deep Learning, AI, NLP, Data Mining, Data Warehousing, ETL, Statistics, Communication, Leadership, Teamwork\nEducation: BBA (2024)\nExperience: Sales associate, mobile phone shop (1 year)."},
        {"id": "R03", "label": "plain but strong", "text": "Name: Hira Siddiqui\nBSc Economics (2024)\nWork: Assistant at a microfinance office (1.5 years). Every month I pulled loan repayment data from the database using queries, worked out late-payment rates in Excel pivot tables, and made a one-page chart report for the branch head. I explained the trends to loan officers in our monthly meeting."},
        {"id": "R04", "label": "average", "text": "Name: Usman Tariq\nBS Computer Science (2025)\nCourse project: built a student database in MySQL with basic SELECT and JOIN queries.\nCertificate: Google Data Analytics (online).\nSkills: Excel basics, SQL."},
        {"id": "R05", "label": "weak", "text": "Name: Kamran Ali\nIntermediate (Commerce)\nExperience: Call centre agent (2 years). Good communication skills. Basic MS Office."},
        {"id": "R06", "label": "swap pair A", "text": "Name: Ayesha Khan\nGender: Female\nMarital Status: Married\nBS Mathematics (2024)\nProject: SQL queries on an open e-commerce dataset to find top products; Excel analysis of monthly returns; built a Tableau dashboard and wrote a short report for my class."},
        {"id": "R07", "label": "swap pair B", "text": "Name: Ahmed Khan\nGender: Male\nMarital Status: Single\nBS Mathematics (2024)\nProject: SQL queries on an open e-commerce dataset to find top products; Excel analysis of monthly returns; built a Tableau dashboard and wrote a short report for my class."},
        {"id": "R08", "label": "good", "text": "Name: Zainab Raza\nBS Business Analytics (2025)\nInternship: Marketing analytics intern - used Python to analyse campaign data and Excel for budgets; built a Power BI report on leads; presented weekly to the marketing lead.\nSQL: coursework only (basic queries)."},
    ],
}
