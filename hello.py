#!/usr/bin/env python3
"""
A robust Hello World application with CLI support, logging, and customization.
Includes time-based greetings, multi-language support, and farewell messages.
"""

import argparse
import logging
import sys
from datetime import datetime
from typing import Optional


# Greeting translations
GREETINGS = {
    "en": {"hello": "Hello", "good_morning": "Good morning", "good_afternoon": "Good afternoon", "good_evening": "Good evening", "goodbye": "Goodbye"},
    "es": {"hello": "Hola", "good_morning": "Buenos días", "good_afternoon": "Buenas tardes", "good_evening": "Buenas noches", "goodbye": "Adiós"},
    "fr": {"hello": "Bonjour", "good_morning": "Bonjour", "good_afternoon": "Bon après-midi", "good_evening": "Bonsoir", "goodbye": "Au revoir"},
    "de": {"hello": "Hallo", "good_morning": "Guten Morgen", "good_afternoon": "Guten Tag", "good_evening": "Guten Abend", "goodbye": "Auf Wiedersehen"},
    "ja": {"hello": "こんにちは", "good_morning": "おはようございます", "good_afternoon": "こんにちは", "good_evening": "こんばんは", "goodbye": "さようなら"},
}


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        verbose: If True, set log level to DEBUG; otherwise INFO.
    
    Returns:
        Configured logger instance.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def get_time_based_greeting(language: str = "en") -> str:
    """
    Get a greeting based on the current time of day.
    
    Args:
        language: Language code for the greeting.
    
    Returns:
        Time-appropriate greeting string.
    """
    hour = datetime.now().hour
    greetings = GREETINGS.get(language, GREETINGS["en"])
    
    if 5 <= hour < 12:
        return greetings["good_morning"]
    elif 12 <= hour < 17:
        return greetings["good_afternoon"]
    elif 17 <= hour < 21:
        return greetings["good_evening"]
    else:
        return greetings["hello"]


def create_farewell(name: Optional[str] = None, language: str = "en", uppercase: bool = False) -> str:
    """
    Create a personalized farewell message.
    
    Args:
        name: Name to bid farewell to. Defaults to "World" if not provided.
        language: Language code for the farewell.
        uppercase: If True, return the farewell in uppercase.
    
    Returns:
        The farewell message.
    """
    if name is None:
        name = "World"
    
    greetings = GREETINGS.get(language, GREETINGS["en"])
    farewell = f"{greetings['goodbye']}, {name}!"
    
    if uppercase:
        farewell = farewell.upper()
    
    return farewell


def create_greeting(name: Optional[str] = None, uppercase: bool = False, language: str = "en", time_based: bool = False) -> str:
    """
    Create a personalized greeting message.
    
    Args:
        name: Name to greet. Defaults to "World" if not provided.
        uppercase: If True, return the greeting in uppercase.
        language: Language code for the greeting (en, es, fr, de, ja).
        time_based: If True, use time-appropriate greeting instead of "Hello".
    
    Returns:
        The greeting message.
    
    Raises:
        ValueError: If name contains invalid characters or language is unsupported.
    """
    if name is None:
        name = "World"
    
    # Validate name
    if name and not all(c.isalnum() or c.isspace() or c in "-'" for c in name):
        raise ValueError(f"Invalid characters in name: {name}")
    
    # Validate language
    if language not in GREETINGS:
        raise ValueError(f"Unsupported language: {language}. Supported: {', '.join(GREETINGS.keys())}")
    
    # Get appropriate greeting
    if time_based:
        greeting_word = get_time_based_greeting(language)
    else:
        greeting_word = GREETINGS[language]["hello"]
    
    greeting = f"{greeting_word}, {name}!"
    
    if uppercase:
        greeting = greeting.upper()
    
    return greeting


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: List of arguments to parse. Uses sys.argv if None.
    
    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="A robust Hello World application",
        epilog="Example: python hello.py --name Alice --uppercase",
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default=None,
        help="Name to greet (default: World)",
    )
    parser.add_argument(
        "-u", "--uppercase",
        action="store_true",
        help="Print greeting in uppercase",
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of times to print the greeting (default: 1)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        default="en",
        choices=["en", "es", "fr", "de", "ja"],
        help="Language for greeting (default: en)",
    )
    parser.add_argument(
        "-t", "--time-based",
        action="store_true",
        help="Use time-appropriate greeting (Good morning/afternoon/evening)",
    )
    parser.add_argument(
        "-f", "--farewell",
        action="store_true",
        help="Include a farewell message after greeting",
    )
    
    return parser.parse_args(args)


def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the application.
    
    Args:
        args: Command-line arguments. Uses sys.argv if None.
    
    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parsed_args = parse_args(args)
    logger = setup_logging(parsed_args.verbose)
    
    logger.info("Starting Hello World application")
    
    try:
        greeting = create_greeting(
            name=parsed_args.name,
            uppercase=parsed_args.uppercase,
            language=parsed_args.language,
            time_based=parsed_args.time_based,
        )
        
        for i in range(parsed_args.count):
            print(greeting)
            logger.info("Printed greeting iteration %d of %d", i + 1, parsed_args.count)
        
        # Print farewell if requested
        if parsed_args.farewell:
            farewell = create_farewell(
                name=parsed_args.name,
                language=parsed_args.language,
                uppercase=parsed_args.uppercase,
            )
            print(farewell)
            logger.info("Printed farewell message")
        
        logger.info("Application completed successfully")
        return 0
        
    except ValueError as e:
        logger.error("Validation error: %s", e)
        return 1
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
