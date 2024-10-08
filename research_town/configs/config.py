from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict


def merge_a_into_b(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    """
    Merge dictionary a into dictionary b recursively.
    """
    for key, value in a.items():
        if isinstance(value, dict) and key in b and isinstance(b[key], dict):
            merge_a_into_b(value, b[key])
        else:
            b[key] = value


class ParamConfig(BaseModel):
    related_paper_num: int = 10
    base_llm: str = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    proj_participant_num: int = 3
    reviewer_num: int = 3
    domain: str = 'computer_vision'
    result_path: str = 'Mixtral-8x7B'
    return_num: Optional[int] = 1
    max_token_num: Optional[int] = 512
    temperature: Optional[float] = 0.0
    top_p: Optional[float] = None
    stream: Optional[bool] = None

    model_config = ConfigDict(
        extra='allow',
    )


class EvalPromptTemplateConfig(BaseModel):
    insight_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the insight based on the following dimensions, considering the current research insights within the research community. '
            'If the research insights field is left blank, please use your common knowledge to assess the insights. Finally, give an overall score (0-100) '
            'and 6 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the insight.\n\n'
            'The details of rating are as follows:\n'
            '1. Novelty\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- How original and unique is the insight?\n'
            '- Does it introduce a new perspective or significant advancement compared to existing methods?\n'
            '- How does it align with or diverge from the innovations highlighted in the insights?\n'
            '2. Validity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does it include solid theoretical foundations, robust algorithms, and detailed methodologies?\n'
            '- Is the method in line with the state-of-the-art techniques noted in the insights?\n'
            '- Are the underlying principles well-defined and logically consistent?\n'
            '- Does the insight demonstrate a deep understanding of relevant theories and concepts?\n'
            '3. Significance\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Evaluate the potential impact of the insight on the specific domain of research community that the insight belongs to and beyond.\n'
            '- How significant is its contribution to advancing the field?\n'
            '- Does it address high-impact problems or gaps identified in the insights?\n'
            '- How applicable is it in practical settings and industry contexts?\n'
            '4. Feasibility\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Assess the feasibility of implementing the insight.\n'
            '- Is it practically applicable in real-world scenarios?\n'
            '- Does it consider efficiency and scalability, in line with the practical application focus of the insights?\n'
            '5. Clarity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Assess the clarity, organization, and presentation quality of the insight.\n'
            '- Is the insight communicated effectively, adhering to high presentation standards seen in top-tier conferences?\n'
            '6. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Consider the ethical implications and societal impact of the insight.\n'
            '- Does it adhere to the growing emphasis on ethical research practices as highlighted in the insights?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the insight to evaluate: {insight}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }
    idea_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the idea based on the following dimensions, considering the current research insights within the research community. '
            'If the research insights field is left blank, please use your common knowledge to assess the insights. Finally, give an overall score (0-100) '
            'and 6 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the idea.\n\n'
            'The details of rating are as follows:\n'
            '1. Novelty\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- How original and unique is the idea?\n'
            '- Does it introduce a new perspective or significant advancement compared to existing methods?\n'
            '- How does it align with or diverge from the innovations highlighted in the insights?\n'
            '2. Validity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does it include solid theoretical foundations, robust algorithms, and detailed methodologies?\n'
            '- Is the method in line with the state-of-the-art techniques noted in the insights?\n'
            '- Are the underlying principles well-defined and logically consistent?\n'
            '- Does the idea demonstrate a deep understanding of relevant theories and concepts?\n'
            '3. Significance\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Evaluate the potential impact of the idea on the specific domain of research community that the idea belongs to and beyond.\n'
            '- How significant is its contribution to advancing the field?\n'
            '- Does it address high-impact problems or gaps identified in the insights?\n'
            '- How applicable is it in practical settings and industry contexts?\n'
            '4. Feasibility\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Assess the feasibility of implementing the idea.\n'
            '- Is it practically applicable in real-world scenarios?\n'
            '- Does it consider efficiency and scalability, in line with the practical application focus of the insights?\n'
            '5. Clarity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Assess the clarity, organization, and presentation quality of the idea.\n'
            '- Is the idea communicated effectively, adhering to high presentation standards seen in top-tier conferences?\n'
            '6. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Consider the ethical implications and societal impact of the idea.\n'
            '- Does it adhere to the growing emphasis on ethical research practices as highlighted in the insights?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the idea to evaluate: {idea}.\nHere is the research insights: {insights}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }
    paper_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the paper draft based on the following dimensions. Finally, give an overall score (0-100) and 6 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the draft.\n\n'
            'The details of rating are as follows:\n'
            '1. Novelty\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the paper introduce a novel problem or new perspective that has not been explored before?\n'
            '- Does it introduce new techniques or significant advancements compared to existing methods?\n'
            '- How does it align with or diverge from the innovations highlighted in the insights?\n'
            '2. Validity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does it include solid theoretical foundations, robust algorithms, and detailed methodologies in addressing the research problem?\n'
            '- Are the underlying principles well-defined and logically consistent?\n'
            '3. Significance\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Evaluate the potential contribution and impact of the paper on the specific domain of research community that the paper belongs to and beyond.\n'
            '- How does it compare to existing works in terms of impact?\n'
            '4. Rigorousness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the research design and methods clearly described and justified?\n'
            '- Is the methodology robust and suitable for addressing the research questions?\n'
            '- Are the results well-analyzed and interpreted?\n'
            '- Do the findings support the claims made in the paper?\n'
            '5. Clarity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Evaluate the clarity, organization, and presentation quality of the paper.\n'
            '- How well do the title and abstract summarize the paper? Are they clear, concise, and informative?\n'
            '- Does it effectively convey the significance and main contributions of the paper?\n'
            '- How well do the title and abstract align with each other? Do they accurately represent the core idea and content of the paper?\n'
            '- Is the content well-structured and easy to follow?\n'
            '6. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Consider the ethical implications and societal impact of the paper.\n'
            '- Does it adhere to ethical guidelines and responsible research practices?\n'
            '- Are potential negative consequences or biases addressed?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the paper draft to evaluate:\npaper: {paper}\nIdea: {idea}\nInsights: {insights}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }
    review_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the review based on the following dimensions. You only need to give an overall score (0-100) and 10 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the review. '
            'For these components that are left blank (for example: rebuttal, meta_review, etc), please provide your common knowledge to assess the review. You must give an overall score with dimension scores. No detailed analysis is needed.\n\n'
            'The details of rating are as follows:\n'
            '1. Summarization\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            "- Does the review accurately summarize the paper's motivation?\n"
            '- Are the key contributions and achievements clearly summarized?\n'
            "- Are there any misunderstandings that need to be addressed in the author's response?\n"
            '2. Strengths\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the strengths of the work clearly described?\n'
            '- Are the claims sound, both theoretically and empirically?\n'
            '- Is the contribution significant and novel?\n'
            '- Is the work relevant to the community?\n'
            '3. Weaknesses\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the limitations of the work clearly explained?\n'
            '- Are the weaknesses addressed along the same axes as the strengths?\n'
            '- Are the criticisms detailed, specific, and polite?\n'
            '4. Correctness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the claims and methods correct?\n'
            '- Is the empirical methodology sound?\n'
            '- Are there any incorrect claims or methods detailed thoroughly?\n'
            '- Is the criticism well-motivated and understandable?\n'
            '5. Clarity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is the paper well-written?\n'
            '- Is the exposition of the paper clear?\n'
            '- What parts of the paper need revision to improve clarity?\n'
            '6. Originality\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is it clearly discussed how this work differs from previous contributions?\n'
            '- Does the submission show due scholarship, relating the proposed work to prior work?\n'
            '- Does the related work section explain how the proposed work differs from prior literature?\n'
            '7. Reproducibility\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are there enough details to reproduce the major results of this work?\n'
            '- Is the work reasonably reproducible?\n'
            '- If not, are the reproducibility issues listed among the weaknesses?\n'
            '8. Significance\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Have the authors adequately addressed the broader impact of their work?\n'
            '- Are potential negative ethical and societal implications considered?\n'
            '9. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the submission raise potential ethical concerns?\n'
            '- Are there methods, applications, or data that create or reinforce unfair bias?\n'
            '- Does the work have a primary purpose of harm or injury?\n'
            '10. Fairness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the review scores distributed fairly?\n'
            '- Is there a balance in the scoring, without significant bias towards extremely high or low scores?\n'
            '- Do the scores reflect a reasonable and unbiased assessment of the paper?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the review to evaluate:\nidea: {idea}\nresearch insights: {insights}\npaper: {paper}\nreview: {review}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }
    rebuttal_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the rebuttal based on the following dimensions. Finally, give an overall score (0-100) and 10 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the review.\n\n'
            'The details of rating are as follows:\n'
            '1. Clarity of Response\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is the rebuttal clear in addressing the criticisms raised in the reviews?\n'
            '- Are the responses to each criticism well-structured and understandable?\n'
            '2. Accuracy and Justification\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the rebuttal claims and justifications adequately supported by evidence?\n'
            '- Are any disagreements or discrepancies with the reviews addressed convincingly?\n'
            '3. Responsiveness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the rebuttal address all major concerns and critiques raised in the reviews?\n'
            '- Are the rebuttal responses thorough and comprehensive?\n'
            '4. Persuasiveness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- How persuasive are the arguments and explanations provided in the rebuttal?\n'
            '- Are the rebuttal responses effective in mitigating concerns and defending the paper?\n'
            '5. Professionalism\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is the tone and language of the rebuttal professional and respectful?\n'
            '- Are there any instances of defensive or dismissive language that need improvement?\n'
            '6. Insightfulness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the rebuttal provide new insights or perspectives that were not fully addressed in the original paper or reviews?\n'
            '7. Overall Improvement\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            "- How much does the rebuttal improve the overall perception and understanding of the paper's strengths and weaknesses?\n"
            '8. Clarity of Contributions\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the contributions of the paper clarified and emphasized in the rebuttal?\n'
            '9. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are there any ethical implications or considerations raised in the rebuttal?\n'
            '10. Balance and Fairness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the rebuttal acknowledge both strengths and weaknesses of the paper in a balanced manner?\n'
            '- Is there fairness in addressing criticisms without bias?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the review to evaluate:\nresearch insights: {insights}\nidea: {idea}\npaper: {paper}\nreviews: {review}\nrebuttal: {rebuttal}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }
    meta_review_quality: Dict[str, Union[str, List[str]]] = {
        'intro': (
            'Please evaluate the review based on the following dimensions. Finally, give an overall score (0-100) and 10 dimension scores (for each dimension, provide a rating (1-10)) as the evaluation for the review.\n\n'
            'The details of rating are as follows:\n'
            '1. Summarization\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the meta-review accurately summarize the strengths and weaknesses of the original reviews?\n'
            '- Are the key points of each review clearly and succinctly summarized?\n'
            '- Are any discrepancies or misunderstandings among the reviews identified and addressed?\n'
            '2. Quality\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the strengths and weaknesses of the reviewed paper clearly identified and appropriately critiqued?\n'
            "- Do the critiques show a deep understanding of the paper's content and contributions?\n"
            '- Are the assessments fair and balanced?\n'
            '3. Consistency and Fairness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is there consistency in evaluating different aspects of the reviewed paper across the reviews?\n'
            '- Are the assessments fair, avoiding significant bias towards any particular aspect of the paper?\n'
            '- Are any conflicting opinions among the reviews reconciled appropriately?\n'
            '4. Constructiveness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are the critiques and suggestions provided in the meta-review constructive and actionable?\n'
            '- Do they offer meaningful insights for improving the reviewed paper or future revisions?\n'
            '- Are the recommendations clear and well-supported by evidence from the reviews?\n'
            '5. Clarity\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is the meta-review well-written and logically organized?\n'
            '- Are the points expressed clearly and effectively?\n'
            '- Is the language appropriate and professional?\n'
            '6. Insightfulness\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the meta-review provide insightful commentary beyond summarizing individual reviews?\n'
            '- Are there novel observations or perspectives that enrich the understanding of the reviewed paper?\n'
            '7. Alignment with Review Criteria\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Does the meta-review align with the evaluation criteria provided by the submission guidelines?\n'
            '- Are all relevant aspects of the reviewed paper adequately covered in the meta-review?\n'
            '8. Justification of Final Decision\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Is the final decision or recommendation based on a thorough analysis of the reviews?\n'
            '- Are the reasons for the recommendation clearly articulated and justified?\n'
            '9. Ethical Considerations\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- Are there any ethical considerations raised in the meta-review regarding the reviewed paper or its reviews?\n'
            '- Are potential biases or conflicts of interest addressed appropriately?\n'
            '10. Overall Impression\n'
            '- Rating (1-10):\n'
            '- Comments:\n'
            '- What is your overall impression of the meta-review?\n'
            '- Does it meet the standards expected for a meta-review in terms of thoroughness, insightfulness, and clarity?\n'
        ),
        'examples': ['', ''],
        'template': 'Here is the review to evaluate:\nresearch insights: {insights}\nidea: {idea}\npaper: {paper}\nreviews: {reviews}\nrebuttals: {rebuttals}\nmeta_review: {meta_review}. The output format should follow these rules: Overall Score of an insight (0-100), with 6 Dimension Scores: [d1, d2, d3, ..., d6], where di is the score of the i-th dimension. An example of output is: Overall Score=89 Dimension Scores=[8,9,9,9,9,9].',
    }

    model_config = ConfigDict(
        extra='allow',
    )


class AgentPromptTemplateConfig(BaseModel):
    write_bio: Dict[str, Union[str, List[str]]] = {
        'intro': "Based on the list of the researcher's first person persona from different times, please write a comprehensive first person persona. Focus more on more recent personas. Be concise and clear (around 300 words).",
        'examples': ['', ''],
        'template': 'Here are the personas from different times: {publication_info}',
    }
    review_literature: Dict[str, Union[str, List[str]]] = {
        'intro': 'Given a biograph of me, target research domain, and some recent paper abstracts, could you summarize the keywords of high-level research backgrounds and insights in this field (related to my profile if possible)?',
        'examples': ['', ''],
        'template': 'Biography:\n {profile_bio}\nResearch domains: {domains}\nRecent paper abstracts: {papers}',
    }
    brainstorm_idea: Dict[str, Union[str, List[str]]] = {
        'intro': 'Here is a high-level summarized insight of a research field. How do you view this field? Do you have any novel ideas or insights? Please give me 3 to 5 novel ideas and insights in bullet points. Each bullet point should be concise, containing 2 or 3 sentences.',
        'examples': ['', ''],
        'template': 'Here is the insight: {insights}',
    }
    discuss_idea: Dict[str, Union[str, List[str]]] = {
        'intro': 'Given a list of research ideas, please summarize them by removing duplicates and resolving any contradictory ideas by selecting the more reasonable one.',
        'examples': ['', ''],
        'template': 'Here are the research ideas:\n{ideas}\n',
    }
    write_proposal: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write a paper based on the following ideas and external data. To save time, you only need to write the abstract. You might use two or more of these ideas if they are related and work well together.',
        'examples': ['', ''],
        'template': 'Here is the idea: {idea}\nHere are the external data, which is a list of abstracts of related papers: {papers}',
    }
    write_review_summary: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write a summary of the paper for the following submission you have made to an academic conference.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}',
    }
    write_review_strength: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write the strength of the paper for the following submission you have made to an academic conference.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere is the summary of the paper: {summary}',
    }
    write_review_weakness: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write the weakness of the paper for the following submission you have made to an academic conference.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere is the summary of the paper: {summary}',
    }
    write_review_score: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please provide a score for the following submission you have made to an academic conference. The score should be between 1 and 10, where 1 is the lowest and 10 is the highest.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere is the summary of the paper: {summary}\nHere is the strength of the paper: {strength}\nHere is the weakness of the paper: {weakness}',
    }
    write_meta_review_summary: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write a summary of the reviews for the following submission you have made to an academic conference. Your summary should summarize the reviews and decisions to help the reviewers to make a decision.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere are the reviews: {reviews}\nHere are the rebuttals: {rebuttals}',
    }
    write_meta_review_strength: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write the strength of the submission for the following submission you have made to an academic conference. Your strength should summarize the reviews and decisions to help the reviewers to make a decision.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere are the reviews: {reviews}\nHere are the rebuttals: {rebuttals}\nHere is the summary of the reviews: {summary}',
    }
    write_meta_review_weakness: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write the weakness of the submission for the following submission you have made to an academic conference. Your weakness should summarize the reviews and decisions to help the reviewers to make a decision.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere are the reviews: {reviews}\nHere are the rebuttals: {rebuttals}\nHere is the summary of the reviews: {summary}',
    }
    write_meta_review_decision: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please make a review decision to decide whether the following submission should be accepted or rejected by an academic conference. Please indicate your review decision as accept or reject.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere are the reviews: {reviews}\nHere are the rebuttals: {rebuttals}\nHere is the summary of the reviews: {summary}\nHere is the strength of the submission: {strength}\nHere is the weakness of the submission: {weakness}',
    }
    write_rebuttal: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please write a rebuttal for the following submission you have made to an academic conference. Your rebuttal should rebut the reviews to convince the reviewers to accept your submission.',
        'examples': ['', ''],
        'template': 'Here is the submission: {paper}\nHere are the reviews: {review}',
    }
    discuss: Dict[str, Union[str, List[str]]] = {
        'intro': 'Please continue in a conversation with other fellow researchers for me, where you will address their concerns in a scholarly way.',
        'examples': ['', ''],
        'template': 'Here are the messages from other researchers: {message}',
    }

    model_config = ConfigDict(
        extra='allow',
    )


class Config(BaseModel):
    param: ParamConfig = ParamConfig()
    agent_prompt_template: AgentPromptTemplateConfig = AgentPromptTemplateConfig()
    eval_prompt_template: EvalPromptTemplateConfig = EvalPromptTemplateConfig()

    model_config = ConfigDict(extra='allow')

    def __init__(self, yaml_config_path: Optional[str] = None, **data: Any) -> None:
        super().__init__(**data)
        if yaml_config_path:
            self.load_from_yaml(yaml_config_path)
        self.check_agent_prompt_template_placeholder()
        self.check_eval_prompt_template_placeholder()

    def load_from_yaml(self, yaml_config_path: str) -> None:
        with open(yaml_config_path, 'r') as f:
            yaml_cfg: Dict[str, Any] = yaml.safe_load(f)
        self.merge_from_other_cfg(yaml_cfg)
        self.check_agent_prompt_template_placeholder()
        self.check_eval_prompt_template_placeholder()

    def save_to_yaml(self, yaml_config_path: str) -> None:
        with open(yaml_config_path, 'w') as f:
            yaml.dump(self.model_dump(), f)

    def check_agent_prompt_template_placeholder(self) -> None:
        templates = self.agent_prompt_template.model_dump()
        required_placeholders = {
            'write_bio': [
                '{publication_info}',
            ],
            'review_literature': ['{profile_bio}', '{domains}', '{papers}'],
            'brainstorm_idea': ['{insights}'],
            'discuss_idea': ['{ideas}'],
            'write_proposal': ['{idea}', '{papers}'],
            'write_review_summary': ['{paper}'],
            'write_review_strength': ['{paper}', '{summary}'],
            'write_review_weakness': ['{paper}', '{summary}'],
            'write_review_score': ['{paper}', '{summary}', '{strength}', '{weakness}'],
            'write_meta_review_summary': ['{paper}', '{reviews}', '{rebuttals}'],
            'write_meta_review_strength': [
                '{paper}',
                '{reviews}',
                '{rebuttals}',
                '{summary}',
            ],
            'write_meta_review_weakness': [
                '{paper}',
                '{reviews}',
                '{rebuttals}',
                '{summary}',
            ],
            'write_meta_review_decision': [
                '{paper}',
                '{reviews}',
                '{rebuttals}',
                '{summary}',
                '{strength}',
                '{weakness}',
            ],
            'write_rebuttal': ['{paper}', '{review}'],
        }

        for template_name, placeholders in required_placeholders.items():
            template = templates.get(template_name, '')['template']
            for placeholder in placeholders:
                assert (
                    placeholder in template
                ), f"Template '{template_name}' is missing placeholder '{placeholder}'"

    def check_eval_prompt_template_placeholder(self) -> None:
        templates = self.eval_prompt_template.model_dump()
        required_placeholders = {
            'insight_quality': ['{insight}'],
            'idea_quality': ['{idea}', '{insights}'],
            'paper_quality': ['{paper}', '{idea}', '{insights}'],
            'review_quality': ['{idea}', '{insights}', '{paper}', '{review}'],
            'rebuttal_quality': [
                '{insights}',
                '{idea}',
                '{paper}',
                '{review}',
                '{rebuttal}',
            ],
            'meta_review_quality': [
                '{insights}',
                '{idea}',
                '{paper}',
                '{reviews}',
                '{rebuttals}',
                '{meta_review}',
            ],
        }

        for template_name, placeholders in required_placeholders.items():
            template = templates.get(template_name, '')['template']
            for placeholder in placeholders:
                assert (
                    placeholder in template
                ), f"Template '{template_name}' is missing placeholder '{placeholder}'"

    def merge_from_other_cfg(self, other_cfg: Dict[str, Any]) -> None:
        if 'param' in other_cfg:
            updated_param = self.param.model_dump()
            merge_a_into_b(other_cfg['param'], updated_param)
            self.param = ParamConfig(**updated_param)
        if 'agent_prompt_template' in other_cfg:
            updated_agent_template = self.agent_prompt_template.model_dump()
            merge_a_into_b(other_cfg['agent_prompt_template'], updated_agent_template)
            self.agent_prompt_template = AgentPromptTemplateConfig(
                **updated_agent_template
            )
        if 'eval_prompt_template' in other_cfg:
            updated_eval_template = self.eval_prompt_template.model_dump()
            merge_a_into_b(other_cfg['eval_prompt_template'], updated_eval_template)
            self.eval_prompt_template = EvalPromptTemplateConfig(
                **updated_eval_template
            )
