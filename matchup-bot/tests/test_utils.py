from bot.utils.prompts import conversation_prompts, premium_prompts

def test_conversation_prompts():
    assert isinstance(conversation_prompts, list)
    assert len(conversation_prompts) > 0

def test_premium_prompts():
    assert isinstance(premium_prompts, list)
    assert len(premium_prompts) > 0
