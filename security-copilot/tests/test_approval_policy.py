import pytest

from config.approval_policy import ApprovalLevel, check_action, require_approval


def test_read_only_actions_are_automatic():
    decision = check_action("repository_scan")
    assert decision.allowed is True
    assert decision.level == ApprovalLevel.AUTOMATIC


def test_destructive_actions_need_human_approval():
    assert check_action("merge_pr").allowed is False
    assert check_action("merge_pr", explicit_approval=True).allowed is True


def test_dangerous_actions_remain_blocked():
    assert check_action("delete_database", explicit_approval=True).allowed is False
    with pytest.raises(PermissionError):
        require_approval("production_deployment", explicit_approval=True)

