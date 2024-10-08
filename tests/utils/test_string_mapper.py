from beartype.typing import Dict, List, Union

from research_town.utils.string_mapper import (
    map_idea_list_to_str,
    map_idea_to_str,
    map_insight_list_to_str,
    map_insight_to_str,
    map_meta_review_list_to_str,
    map_meta_review_to_str,
    map_paper_list_to_str,
    map_paper_to_str,
    map_rebuttal_to_str,
    map_review_list_to_str,
    map_review_to_str,
)


def test_map_idea_list_to_str() -> None:
    ideas = [{'content': 'Idea 1'}, {'content': 'Idea 2'}, {'content': 'Idea 3'}]
    expected_result = 'Idea 1Idea 2Idea 3'
    assert map_idea_list_to_str(ideas) == expected_result


def test_map_idea_to_str() -> None:
    idea = {'content': 'This is an idea'}
    expected_result = 'This is an idea'
    assert map_idea_to_str(idea) == expected_result


def test_map_paper_list_to_str() -> None:
    papers = [
        {'abstract': 'Abstract 1'},
        {'abstract': 'Abstract 2'},
        {'abstract': 'Abstract 3'},
    ]
    expected_result = 'Paper: Abstract 1Paper: Abstract 2Paper: Abstract 3'
    assert map_paper_list_to_str(papers) == expected_result


def test_map_review_list_to_str() -> None:
    reviews: List[Dict[str, Union[int, str]]] = [
        {
            'score': 5,
            'summary': 'Review 1',
            'strength': 'Strength 1',
            'weakness': 'Weakness 1',
        },
        {
            'score': 3,
            'summary': 'Review 2',
            'strength': 'Strength 2',
            'weakness': 'Weakness 2',
        },
        {
            'score': 4,
            'summary': 'Review 3',
            'strength': 'Strength 3',
            'weakness': 'Weakness 3',
        },
    ]
    expected_result = 'Score: 5\nSummary: Review 1\nStrength: Strength 1\nWeakness: Weakness 1Score: 3\nSummary: Review 2\nStrength: Strength 2\nWeakness: Weakness 2Score: 4\nSummary: Review 3\nStrength: Strength 3\nWeakness: Weakness 3'
    assert map_review_list_to_str(reviews) == expected_result


def test_map_paper_to_str() -> None:
    paper = {'abstract': 'This is a paper abstract'}
    expected_result = 'Paper: This is a paper abstract'
    assert map_paper_to_str(paper) == expected_result


def test_map_rebuttal_to_str() -> None:
    rebuttal = {'content': 'This is a rebuttal'}
    expected_result = 'Rebuttal: This is a rebuttal'
    assert map_rebuttal_to_str(rebuttal) == expected_result


def test_map_review_to_str() -> None:
    review: Dict[str, Union[int, str]] = {
        'score': 4,
        'summary': 'This is a review',
        'strength': 'Strength',
        'weakness': 'Weakness',
    }
    expected_result = (
        'Score: 4\nSummary: This is a review\nStrength: Strength\nWeakness: Weakness'
    )
    assert map_review_to_str(review) == expected_result


def test_map_meta_review_to_str() -> None:
    meta_review = {
        'summary': 'This is a meta review',
        'strength': 'Strength',
        'weakness': 'Weakness',
        'decision': 'accept',
    }
    expected_result = 'Summary: This is a meta review\nStrength: Strength\nWeakness: Weakness\nDecision: accept'
    assert map_meta_review_to_str(meta_review) == expected_result


def test_map_meta_review_list_to_str() -> None:
    meta_reviews = [
        {
            'summary': 'Meta review 1',
            'strength': 'Strength 1',
            'weakness': 'Weakness 1',
            'decision': 'accept',
        },
        {
            'summary': 'Meta review 2',
            'strength': 'Strength 2',
            'weakness': 'Weakness 2',
            'decision': 'reject',
        },
        {
            'summary': 'Meta review 3',
            'strength': 'Strength 3',
            'weakness': 'Weakness 3',
            'decision': 'accept',
        },
    ]
    expected_result = 'Summary: Meta review 1\nStrength: Strength 1\nWeakness: Weakness 1\nDecision: acceptSummary: Meta review 2\nStrength: Strength 2\nWeakness: Weakness 2\nDecision: rejectSummary: Meta review 3\nStrength: Strength 3\nWeakness: Weakness 3\nDecision: accept'
    assert map_meta_review_list_to_str(meta_reviews) == expected_result


def test_map_insight_list_to_str() -> None:
    insights = [
        {'content': 'Insight 1'},
        {'content': 'Insight 2'},
        {'content': 'Insight 3'},
    ]
    expected_result = 'Insight 1Insight 2Insight 3'
    assert map_insight_list_to_str(insights) == expected_result


def test_map_insight_to_str() -> None:
    insight = {'content': 'This is an insight'}
    expected_result = 'This is an insight'
    assert map_insight_to_str(insight) == expected_result
