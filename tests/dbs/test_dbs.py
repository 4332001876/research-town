import json
import pickle
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import torch
from beartype.typing import Any, Dict, List

from research_town.configs import Config
from research_town.dbs import (
    AgentAgentIdeaDiscussionLog,
    AgentPaperMetaReviewWritingLog,
    AgentPaperRebuttalWritingLog,
    AgentPaperReviewWritingLog,
    AgentProfile,
    AgentProfileDB,
    EnvLogDB,
    PaperProfile,
    PaperProfileDB,
    ProgressDB,
    ResearchIdea,
)
from tests.mocks.mocking_func import mock_prompting


def test_envlogdb_basic() -> None:
    db = EnvLogDB()
    review_log = AgentPaperReviewWritingLog(
        paper_pk='paper1',
        agent_pk='agent1',
        score=5,
        summary='Good paper',
        strength='Interesting',
        weakness='None',
    )
    rebuttal_log = AgentPaperRebuttalWritingLog(
        paper_pk='paper1',
        agent_pk='agent1',
        rebuttal_content='I disagree with the review',
    )
    meta_review_log = AgentPaperMetaReviewWritingLog(
        paper_pk='paper1',
        agent_pk='agent1',
        decision=True,
        summary='Good paper',
        strength='Interesting',
        weakness='None',
    )
    discussion_log = AgentAgentIdeaDiscussionLog(
        agent_from_pk='agent1',
        agent_from_name='Rex Ying',
        agent_to_pk='agent2',
        agent_to_name='John Doe',
        message="Let's discuss this paper",
    )

    db.add(review_log)
    db.add(rebuttal_log)
    db.add(meta_review_log)
    db.add(discussion_log)

    new_review_log = AgentPaperReviewWritingLog(
        paper_pk='paper1',
        agent_pk='agent2',
        score=4,
        summary='Interesting paper',
        strength='Good',
        weakness='None',
    )
    db.add(new_review_log)
    assert new_review_log.pk in db.dbs['AgentPaperReviewWritingLog'].data
    assert len(db.dbs['AgentPaperReviewWritingLog'].data) == 2

    conditions: Dict[str, Any] = {'paper_pk': 'paper1'}
    results = db.get(AgentPaperReviewWritingLog, **conditions)
    assert len(results) == 2
    assert results[0].summary == 'Good paper'
    assert results[0].strength == 'Interesting'
    assert results[0].weakness == 'None'

    updates = {
        'score': 3,
        'summary': 'Bad paper',
        'strength': 'None',
        'weakness': 'Really?',
    }
    updated_conditions = {'paper_pk': 'paper1'}
    updated_count = db.update(AgentPaperReviewWritingLog, updates, **updated_conditions)
    assert updated_count == 2

    updated_log = db.get(AgentPaperReviewWritingLog, **conditions)[0]

    assert updated_log.score == 3
    assert updated_log.summary == 'Bad paper'
    assert updated_log.strength == 'None'
    assert updated_log.weakness == 'Really?'

    delete_conditions = {'paper_pk': 'paper1', 'agent_pk': 'agent1'}
    deleted_count = db.delete(AgentPaperReviewWritingLog, **delete_conditions)
    assert deleted_count == 1

    results = db.get(AgentPaperReviewWritingLog, **conditions)
    assert len(results) == 1

    with TemporaryDirectory() as temp_dir:
        db.save_to_json(temp_dir)

        new_db = EnvLogDB()
        new_db.load_from_json(temp_dir)

        assert len(new_db.dbs['AgentPaperReviewWritingLog'].data) == 1
        assert len(new_db.dbs['AgentPaperRebuttalWritingLog'].data) == 1
        assert len(new_db.dbs['AgentPaperMetaReviewWritingLog'].data) == 1
        assert len(new_db.dbs['AgentAgentIdeaDiscussionLog'].data) == 1
        assert (
            new_db.dbs['AgentPaperReviewWritingLog'].data[new_review_log.pk].summary
            == 'Bad paper'
        )


def test_progressdb_basic() -> None:
    db = ProgressDB()
    idea1 = ResearchIdea(content='Idea for a new AI algorithm')
    idea2 = ResearchIdea(content='Quantum computing research plan')

    db.add(idea1)
    db.add(idea2)

    new_idea = ResearchIdea(content='Blockchain research proposal')
    db.add(new_idea)
    assert new_idea.pk in db.dbs['ResearchIdea'].data

    content: Dict[str, Any] = {'content': 'Idea for a new AI algorithm'}
    results = db.get(ResearchIdea, **content)
    assert len(results) == 1
    assert results[0].content == 'Idea for a new AI algorithm'

    updates = {'content': 'Updated idea content'}
    conditions = {'content': 'Idea for a new AI algorithm'}
    updated_count = db.update(ResearchIdea, updates, **conditions)
    assert updated_count == 1
    content2: Dict[str, Any] = {'content': 'Updated idea content'}
    updated_results = db.get(ResearchIdea, **content2)
    assert len(updated_results) == 1
    assert updated_results[0].content == 'Updated idea content'

    content3: Dict[str, Any] = {'content': 'Quantum computing research plan'}
    deleted_count = db.delete(ResearchIdea, **content3)
    assert deleted_count == 1
    remaining_results = db.get(ResearchIdea, **content3)
    assert len(remaining_results) == 0

    with TemporaryDirectory() as temp_dir:
        db.save_to_json(temp_dir)

        new_db = ProgressDB()
        new_db.load_from_json(temp_dir)

        assert len(new_db.dbs['ResearchIdea'].data) == 2


def test_agentprofiledb_basic() -> None:
    db = AgentProfileDB()
    agent1 = AgentProfile(
        name='John Doe', bio='Researcher in AI', institute='AI Institute'
    )
    agent2 = AgentProfile(name='Jane Smith', bio='Expert in NLP', institute='NLP Lab')
    db.add(agent1)
    db.add(agent2)

    agent3 = AgentProfile(
        name='Alice Johnson', bio='Data Scientist', institute='Data Lab'
    )
    db.add(agent3)
    assert agent3.pk in db.data
    assert db.data[agent3.pk].name == 'Alice Johnson'

    updates = {'bio': 'Senior Researcher in AI'}
    success = db.update(agent1.pk, updates)

    assert success
    assert db.data[agent1.pk].bio == 'Senior Researcher in AI'

    success = db.update('non-existing-pk', {'bio': 'New Bio'})
    assert not success

    success = db.delete(agent1.pk)
    assert success
    assert agent1.pk not in db.data

    success = db.delete('non-existing-pk')
    assert not success

    conditions: Dict[str, str] = {'name': 'Jane Smith'}

    results: List[AgentProfile] = db.get(**conditions)

    assert len(results) == 1
    assert results[0].name == 'Jane Smith'

    with TemporaryDirectory() as temp_dir:
        db.save_to_json(temp_dir)


def test_paperprofiledb_basic() -> None:
    db = PaperProfileDB()
    paper1 = PaperProfile(
        title='Sample Paper 1',
        abstract='This is the abstract for paper 1',
        authors=['Author A', 'Author B'],
        url='http://example.com/paper1',
        timestamp=1617181723,
        keywords=['AI', 'ML'],
        domain='Computer Science',
        citation_count=10,
    )
    paper2 = PaperProfile(
        title='Sample Paper 2',
        abstract='This is the abstract for paper 2',
        authors=['Author C'],
        url='http://example.com/paper2',
        timestamp=1617181756,
        keywords=['Quantum Computing'],
        domain='Physics',
        citation_count=5,
    )
    db.add(paper1)
    db.add(paper2)

    new_paper = PaperProfile(
        title='Sample Paper 3',
        abstract='This is the abstract for paper 3',
        authors=['Author D'],
        url='http://example.com/paper3',
        timestamp=1617181789,
        keywords=['Blockchain'],
        domain='Computer Science',
        citation_count=2,
    )
    db.add(new_paper)
    assert new_paper.pk in db.data

    conditions = {'pk': paper1.pk}
    paper: PaperProfile = db.get(**conditions)[0]
    assert paper is not None
    assert paper.title == 'Sample Paper 1'

    updates: Dict[str, Any] = {'title': 'Updated Sample Paper 1', 'citation_count': 15}

    result = db.update(paper1.pk, updates)
    assert result

    conditions = {'pk': paper1.pk}
    updated_paper: PaperProfile = db.get(**conditions)[0]
    assert updated_paper is not None
    assert updated_paper.title == 'Updated Sample Paper 1'
    assert updated_paper.citation_count == 15

    result = db.delete(paper2.pk)
    assert result

    domain: Dict[str, Any] = {'domain': 'Computer Science'}
    results: List[PaperProfile] = db.get(**domain)
    assert len(results) == 2
    assert results[0].title == 'Updated Sample Paper 1'
    assert results[1].title == 'Sample Paper 3'

    with TemporaryDirectory() as temp_dir:
        db.save_to_json(temp_dir)

        new_db = PaperProfileDB()
        new_db.load_from_json(temp_dir)

        assert len(new_db.data) == 2
        assert paper1.pk in new_db.data
        assert new_db.data[paper1.pk].title == 'Updated Sample Paper 1'


def test_agent_match() -> None:
    db = AgentProfileDB()
    agent1 = AgentProfile(
        name='John Doe', bio='Researcher in AI', institute='AI Institute'
    )
    agent2 = AgentProfile(name='Jane Smith', bio='Expert in NLP', institute='NLP Lab')
    agent3 = AgentProfile(name='Jane kid', bio='Expert in RL', institute='RL Lab')
    agent_profile_l = [agent1, agent2, agent3]
    lead_agent_profile = 'Researcher in CV'
    match_agent_profiles = db.match(
        query=lead_agent_profile, agent_profiles=agent_profile_l, num=2
    )
    assert match_agent_profiles
    assert len(match_agent_profiles) == 2


def test_paper_match() -> None:
    db = PaperProfileDB()
    paper1 = PaperProfile(
        title='Sample Paper 1',
        abstract='This is the abstract for paper 1',
        authors=['Author A', 'Author B'],
        url='http://example.com/paper1',
        timestamp=1617181723,
        keywords=['AI', 'ML'],
        domain='Computer Science',
        citation_count=10,
    )
    paper2 = PaperProfile(
        title='Sample Paper 2',
        abstract='This is the abstract for paper 2',
        authors=['Author C'],
        url='http://example.com/paper2',
        timestamp=1617181756,
        keywords=['Quantum Computing'],
        domain='Physics',
        citation_count=5,
    )
    paper_3 = PaperProfile(
        title='Sample Paper 3',
        abstract='This is the abstract for paper 3',
        authors=['Author D'],
        url='http://example.com/paper3',
        timestamp=1617181789,
        keywords=['Blockchain'],
        domain='Computer Science',
        citation_count=2,
    )
    agent_profile_l = [paper1, paper2, paper_3]
    lead_agent_profile = 'Researcher in CV'
    match_paper_profiles = db.match(
        query=lead_agent_profile, paper_profiles=agent_profile_l, num=2
    )
    assert match_paper_profiles
    assert len(match_paper_profiles) == 2


def test_agent_file() -> None:
    db = AgentProfileDB()
    agent1 = AgentProfile(
        name='John Doe', bio='Researcher in AI', institute='AI Institute'
    )
    agent2 = AgentProfile(name='Jane Smith', bio='Expert in NLP', institute='NLP Lab')
    db.add(agent1)
    db.add(agent2)
    # save without embeddings
    db.save_to_json('data/test')
    with open('data/test/AgentProfileDB.json', 'r') as f:
        data_test = json.load(f)
    assert len(data_test) > 0
    assert db.data == {pk: AgentProfile(**data) for pk, data in data_test.items()}
    # load without embeddings
    db_test = AgentProfileDB()
    db_test.load_from_json('data/test')
    assert db.data == db_test.data
    # save with embeddings
    db.transform_to_embed()
    db.save_to_json('data/test', with_embed=True)
    with open('data/test/AgentProfileDB.pkl', 'rb') as f:
        data_embed_test = pickle.load(f)
    assert db.data_embed.keys() == data_embed_test.keys()
    for agent_pk in db.data_embed:
        assert torch.equal(db.data_embed[agent_pk], data_embed_test[agent_pk])
    # load with embeddings
    db_test = AgentProfileDB()
    db_test.load_from_json('data/test', with_embed=True)
    assert db.data_embed.keys() == db_test.data_embed.keys()
    for agent_pk in db.data_embed:
        assert torch.equal(db.data_embed[agent_pk], db_test.data_embed[agent_pk])
    # delete test file
    shutil.rmtree('data/test')


def test_paper_file() -> None:
    db = PaperProfileDB()
    paper1 = PaperProfile(
        title='Sample Paper 1',
        abstract='This is the abstract for paper 1',
        authors=['Author A', 'Author B'],
        url='http://example.com/paper1',
        timestamp=1617181723,
        keywords=['AI', 'ML'],
        domain='Computer Science',
        citation_count=10,
    )
    paper2 = PaperProfile(
        title='Sample Paper 2',
        abstract='This is the abstract for paper 2',
        authors=['Author C'],
        url='http://example.com/paper2',
        timestamp=1617181756,
        keywords=['Quantum Computing'],
        domain='Physics',
        citation_count=5,
    )
    db.add(paper1)
    db.add(paper2)
    # save without embeddings
    db.save_to_json('data/test')
    with open('data/test/PaperProfileDB.json', 'r') as f:
        data_test = json.load(f)
    assert len(data_test) > 0
    assert db.data == {pk: PaperProfile(**data) for pk, data in data_test.items()}
    # load without embeddings
    db_test = PaperProfileDB()
    db_test.load_from_json('data/test')
    assert db.data == db_test.data
    # save with embeddings
    db.transform_to_embed()
    db.save_to_json('data/test', with_embed=True)
    with open('data/test/PaperProfileDB.pkl', 'rb') as f:
        data_embed_test = pickle.load(f)
    assert db.data_embed.keys() == data_embed_test.keys()
    for paper_pk in db.data_embed:
        assert torch.equal(db.data_embed[paper_pk], data_embed_test[paper_pk])
    # load with embeddings
    db_test = PaperProfileDB()
    db_test.load_from_json('data/test', with_embed=True)
    assert db.data_embed.keys() == db_test.data_embed.keys()
    for paper_pk in db.data_embed:
        assert torch.equal(db.data_embed[paper_pk], db_test.data_embed[paper_pk])
    # delete test file
    shutil.rmtree('data/test')


@patch('research_town.utils.agent_prompter.model_prompting')
def test_pull_agents(mock_model_prompting: MagicMock) -> None:
    mock_model_prompting.side_effect = mock_prompting

    db = AgentProfileDB()
    agent_names = ['Jiaxuan You', 'Jure Leskovec']
    db.pull_agents(agent_names=agent_names, config=Config())
    assert db.data.keys()
    assert len(db.data.keys()) == 2
    assert db.data.values()


def test_pull_papers() -> None:
    db = PaperProfileDB()
    db.pull_papers(num=2, domain='Data Mining')
    assert db.data.keys()
    assert len(db.data.keys()) == 2
    assert db.data.values()
