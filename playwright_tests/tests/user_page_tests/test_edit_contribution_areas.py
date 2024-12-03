import allure
import pytest
from pytest_check import check
from playwright.sync_api import Page

from playwright_tests.core.utilities import Utilities
from playwright_tests.messages.mess_system_pages_messages.edit_cont_areas_page_messages import (
    EditContributionAreasPageMessages)
from playwright_tests.messages.my_profile_pages_messages.my_profile_page_messages import (
    MyProfileMessages)
from playwright_tests.pages.sumo_pages import SumoPages


# T5697937
@pytest.mark.userContributionTests
def test_all_checkboxes_can_be_selected_and_saved(page: Page):
    utilities = Utilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin account"):
        utilities.start_existing_session(utilities.username_extraction_from_email(
            utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))
    original_user = sumo_pages.top_navbar.get_text_of_logged_in_username()

    with allure.step("Checking all contributor checkboxes"):
        sumo_pages.edit_profile_flow.check_all_profile_contribution_areas(checked=False)

    with check, allure.step("Verifying that the correct notification banner text is displayed"):
        assert sumo_pages.edit_my_profile_con_areas_page.edit_con_areas_pref_banner_txt(
        ) == EditContributionAreasPageMessages.PREFERENCES_SAVED_NOTIFICATION_BANNER_TEXT

    with allure.step("Verifying that all the checkboxes are checked"):
        assert (
            sumo_pages.edit_my_profile_con_areas_page.are_all_cont_pref_checked()
        ), "Not all checkbox options are checked!"

    contribution_options = (sumo_pages.edit_my_profile_con_areas_page
                            .get_contrib_areas_checkbox_labels())

    with allure.step("Accessing the my profile page and verifying that the displayed groups are "
                     "the correct ones"):
        sumo_pages.user_navbar.click_on_my_profile_option()
        for option in contribution_options:
            assert option in (sumo_pages.my_profile_page.get_my_profile_groups_items_text())

    with allure.step("Signing in with a different account and verifying that the original user "
                     "groups are displayed"):
        utilities.start_existing_session(utilities.username_extraction_from_email(
            utilities.user_secrets_accounts['TEST_ACCOUNT_13']
        ))

    with allure.step("Navigating to the user page and verifying that the user groups is "
                     "successfully displayed"):
        utilities.navigate_to_link(MyProfileMessages.get_my_profile_stage_url(original_user))
        for option in contribution_options:
            assert option in (sumo_pages.my_profile_page.get_my_profile_groups_items_text())

    with allure.step("Signing in back with the original user"):
        utilities.start_existing_session(utilities.username_extraction_from_email(
            utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))

    with allure.step("Accessing the edit contribution areas page and unchecking all checkboxes"):
        sumo_pages.edit_profile_flow.check_all_profile_contribution_areas(checked=True)

    with check, allure.step("Clicking on the update button and verifying that the correct "
                            "notification banner is displayed"):
        assert sumo_pages.edit_my_profile_con_areas_page.edit_con_areas_pref_banner_txt(
        ) == EditContributionAreasPageMessages.PREFERENCES_SAVED_NOTIFICATION_BANNER_TEXT

    with allure.step("Verifying that the profile groups section is no longer displayed inside the "
                     "profile section"):
        sumo_pages.user_navbar.click_on_my_profile_option()
        for option in contribution_options:
            assert option not in (sumo_pages.my_profile_page.get_my_profile_groups_items_text())

    with allure.step("Logging in with a different user and accessing the original user profile"):
        utilities.start_existing_session(utilities.username_extraction_from_email(
            utilities.user_secrets_accounts['TEST_ACCOUNT_13']
        ))

    with allure.step("Navigating to the my profile page and verifying that the added groups are "
                     "no longer displayed"):
        utilities.navigate_to_link(MyProfileMessages.get_my_profile_stage_url(original_user))
        for option in contribution_options:
            assert option not in (sumo_pages.my_profile_page.get_my_profile_groups_items_text())
