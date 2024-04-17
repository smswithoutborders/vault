"""Module for proving ownership of phone numbers using various 2FA APIs."""

import logging
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    CUSTOM_OWNERSHIP_API_KEY,
    CUSTOM_OWNERSHIP_API_URL,
)

logger = logging.getLogger(__name__)


class ProveOfOwnership:
    """
    A class for proving ownership of a phone number using various 2FA APIs.

    Attributes:
        api_key (str): API key for the custom 2FA service.
        api_url (str): URL endpoint for the custom 2FA service.
        twilio_account_sid (str): Twilio account SID.
        twilio_auth_token (str): Twilio authentication token.
        twilio_phone_number (str): Twilio phone number used for sending SMS.

    Methods:
        send_verification_code(phone_number): Sends a verification code to the
            given phone number.
        verify_code(phone_number, code): Verifies the provided code against the
            sent verification code.
    """

    def __init__(self):
        """Initialize the ProveOfOwnership."""
        self.api_key = CUSTOM_OWNERSHIP_API_KEY
        self.api_url = CUSTOM_OWNERSHIP_API_URL
        self.twilio_account_sid = TWILIO_ACCOUNT_SID
        self.twilio_auth_token = TWILIO_AUTH_TOKEN
        self.twilio_phone_number = TWILIO_PHONE_NUMBER
        self.twilio_client = None
        if (
            self.twilio_account_sid
            and self.twilio_auth_token
            and self.twilio_phone_number
        ):
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_verification_code(self, phone_number):
        """
        Sends a verification code to the given phone number.

        Args:
            phone_number (str): The phone number to send the verification code to.

        Returns:
            bool: True if the code is sent successfully, False otherwise.
        """
        if self.twilio_client is not None:
            try:
                verification = self.twilio_client.verify.v2.services(
                    self.twilio_account_sid
                ).verifications.create(to=phone_number, channel="sms")

                logger.info("Verification code sent successfully via Twilio!")
                return True

            except TwilioRestException as e:
                logger.error("Failed to verify code via Twilio: %s", e)
                return False

            except Exception as e:
                logger.error(
                    "Unexpected error occurred while verifying code via Twilio:"
                )
                raise e

        elif self.api_key and self.api_url:
            try:
                response = requests.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"phone_number": phone_number},
                    timeout=10,
                )
                response.raise_for_status()
                logger.info("Verification code sent successfully!")
                return True

            except requests.exceptions.RequestException as e:
                logger.error("Failed to verify code: %s", e)
                return False

            except Exception as e:
                logger.error(
                    "Unexpected error occurred while verifying code via API:",
                )
                raise

        else:
            raise RuntimeError("No valid 2FA service available.")

    def verify_code(self, phone_number, code):
        """
        Verifies the provided code against the sent verification code.

        Args:
            phone_number (str): The phone number that received the verification code.
            code (str): The code to be verified.

        Returns:
            bool: True if the provided code matches the verification code, False otherwise.
        """
        if self.twilio_client is not None:
            try:
                verification_check = self.twilio_client.verify.v2.services(
                    self.twilio_account_sid
                ).verification_checks.create(to=phone_number, code=code)

                if verification_check.status == "approved":
                    logger.info("Verification successful via Twilio!")
                    return True

                logger.error("Verification failed via Twilio. Incorrect code.")
                return False

            except TwilioRestException as e:
                logger.error("Failed to verify code via Twilio: %s", e)
                return False

            except Exception as e:
                logger.error(
                    "Unexpected error occurred while verifying code via Twilio:"
                )
                raise e

        elif self.api_key and self.api_url:
            try:
                verification_check = requests.post(
                    f"{self.api_url}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"phone_number": phone_number, "code": code},
                    timeout=10,
                )

                verification_check.raise_for_status()

                if verification_check.status_code == 200:
                    logger.info("Verification successful!")
                    return True

                logger.error("Verification failed. Incorrect code.")
                return False

            except requests.exceptions.RequestException as e:
                logger.error("Failed to verify code: %s", e)
                return False

            except Exception as e:
                logger.error(
                    "Unexpected error occurred while verifying code via API:",
                )
                raise

        else:
            raise RuntimeError("No valid 2FA service available.")
