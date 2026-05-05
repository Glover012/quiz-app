from typing import Any, ClassVar

import logging
import requests

logger = logging.getLogger(__name__)


class OpenTriviaClientError(Exception):
    """Raised when fetching questions from OpenTDB fails."""


class OpenTriviaClient:
    """HTTP client for fetching quiz questions from the OpenTDB API."""

    BASE_URL: ClassVar[str] = 'https://opentdb.com/api.php'

    def get_questions_data(
            self,
            amount: int | str = 1,
            category: str = '',
            difficulty: str = '',
            question_type: str = '',
            ) -> dict[str, Any]:
        """Load quiz questions data from OpenTDB API based on given parameters."""
        params = {
            'amount' : amount
        }
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        if question_type:
            params['type'] = question_type

        logger.debug("Fetching questions from OpenTDB with params: %s", params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            logger.debug("OpenTDB response status: %s", response.status_code)
            response.raise_for_status()
            data = response.json()
            if not data['results']:
                raise OpenTriviaClientError('No questions found for selected parameters. Try different category, difficulty or type.')
            elif int(amount) > len(data['results']):
                raise OpenTriviaClientError('Not enough questions found for the selected parameters. Try lower number.')
            return data
   
        except requests.exceptions.Timeout as error:
            raise OpenTriviaClientError('Request to OpenTDB timed out.') from error

        except requests.exceptions.ConnectionError as error:
            raise OpenTriviaClientError('Could not connect to OpenTDB.') from error

        except requests.exceptions.HTTPError as error:
            raise OpenTriviaClientError('OpenTDB returned HTTP error.') from error

        except ValueError as error:
            raise OpenTriviaClientError('OpenTDB returned invalid JSON.') from error
