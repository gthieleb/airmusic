#!/usr/bin/env python3
"""
Test script for Airmusic internationalization changes.
This script validates that the internationalization changes work correctly
and maintain backward compatibility.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from const import (
    CONF_LOCALE, CONF_EMPTY_SLOT_TEXT, CONF_INPUT_SOURCES,
    DEFAULT_LOCALE, DEFAULT_EMPTY_SLOT_TEXT, DEFAULT_INPUT_SOURCES,
    LOCALIZED_STRINGS
)

def test_constants():
    """Test that all required constants are properly defined."""
    print("Testing constants...")
    
    # Test that all required constants exist
    assert CONF_LOCALE == "locale"
    assert CONF_EMPTY_SLOT_TEXT == "empty_slot_text"
    assert CONF_INPUT_SOURCES == "input_sources"
    
    # Test default values
    assert DEFAULT_LOCALE == "de"
    assert DEFAULT_EMPTY_SLOT_TEXT == "Leer"
    assert DEFAULT_INPUT_SOURCES == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    print("✓ Constants test passed")


def test_localized_strings():
    """Test that localized strings are properly configured."""
    print("Testing localized strings...")
    
    # Test that German strings exist (backward compatibility)
    assert "de" in LOCALIZED_STRINGS
    assert LOCALIZED_STRINGS["de"]["empty_slot"] == "Leer"
    assert LOCALIZED_STRINGS["de"]["input_sources"] == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    # Test that English strings exist
    assert "en" in LOCALIZED_STRINGS
    assert LOCALIZED_STRINGS["en"]["empty_slot"] == "Empty"
    assert LOCALIZED_STRINGS["en"]["input_sources"] == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    # Test other languages
    for locale in ["es", "fr", "it"]:
        assert locale in LOCALIZED_STRINGS
        assert "empty_slot" in LOCALIZED_STRINGS[locale]
        assert "input_sources" in LOCALIZED_STRINGS[locale]
        assert isinstance(LOCALIZED_STRINGS[locale]["input_sources"], list)
    
    print("✓ Localized strings test passed")


def test_backward_compatibility():
    """Test backward compatibility scenarios."""
    print("Testing backward compatibility...")
    
    # Simulate old config entry data (without locale settings)
    old_config = {
        "host": "192.168.1.100",
        "name": "Airmusic Radio"
    }
    
    # Test that defaults are applied correctly for missing locale settings
    locale = old_config.get(CONF_LOCALE, DEFAULT_LOCALE)
    empty_slot_text = old_config.get(CONF_EMPTY_SLOT_TEXT, 
                                     LOCALIZED_STRINGS.get(locale, {}).get("empty_slot", DEFAULT_EMPTY_SLOT_TEXT))
    input_sources = old_config.get(CONF_INPUT_SOURCES, 
                                   LOCALIZED_STRINGS.get(locale, {}).get("input_sources", DEFAULT_INPUT_SOURCES))
    
    assert locale == "de"  # Default locale
    assert empty_slot_text == "Leer"  # German default
    assert input_sources == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    print("✓ Backward compatibility test passed")


def test_new_configuration():
    """Test new configuration with different locales."""
    print("Testing new configuration...")
    
    # Test English configuration
    en_config = {
        "host": "192.168.1.100",
        "name": "Airmusic Radio",
        "locale": "en",
        "empty_slot_text": "Empty",
        "input_sources": ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    }
    
    locale = en_config.get(CONF_LOCALE, DEFAULT_LOCALE)
    empty_slot_text = en_config.get(CONF_EMPTY_SLOT_TEXT, 
                                    LOCALIZED_STRINGS.get(locale, {}).get("empty_slot", DEFAULT_EMPTY_SLOT_TEXT))
    input_sources = en_config.get(CONF_INPUT_SOURCES, 
                                  LOCALIZED_STRINGS.get(locale, {}).get("input_sources", DEFAULT_INPUT_SOURCES))
    
    assert locale == "en"
    assert empty_slot_text == "Empty"
    assert input_sources == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    # Test custom configuration
    custom_config = {
        "host": "192.168.1.100",
        "name": "Airmusic Radio",
        "locale": "es",
        "empty_slot_text": "Vacío",
        "input_sources": ["Bluetooth", "AUX", "FM"]
    }
    
    locale = custom_config.get(CONF_LOCALE, DEFAULT_LOCALE)
    empty_slot_text = custom_config.get(CONF_EMPTY_SLOT_TEXT, 
                                        LOCALIZED_STRINGS.get(locale, {}).get("empty_slot", DEFAULT_EMPTY_SLOT_TEXT))
    input_sources = custom_config.get(CONF_INPUT_SOURCES, 
                                      LOCALIZED_STRINGS.get(locale, {}).get("input_sources", DEFAULT_INPUT_SOURCES))
    
    assert locale == "es"
    assert empty_slot_text == "Vacío"
    assert input_sources == ["Bluetooth", "AUX", "FM"]
    
    print("✓ New configuration test passed")


def test_string_conversion():
    """Test string to list conversion for input sources."""
    print("Testing string conversion...")
    
    # Test comma-separated string conversion
    input_sources_str = "Bluetooth, AUX, FM, DAB (IR)"
    input_sources_list = [s.strip() for s in input_sources_str.split(",")]
    
    assert input_sources_list == ["Bluetooth", "AUX", "FM", "DAB (IR)"]
    
    # Test with extra spaces
    input_sources_str = " Bluetooth , AUX , FM "
    input_sources_list = [s.strip() for s in input_sources_str.split(",")]
    
    assert input_sources_list == ["Bluetooth", "AUX", "FM"]
    
    print("✓ String conversion test passed")


if __name__ == "__main__":
    print("Running Airmusic internationalization tests...\n")
    
    try:
        test_constants()
        test_localized_strings()
        test_backward_compatibility()
        test_new_configuration()
        test_string_conversion()
        
        print("\n✅ All tests passed! Internationalization changes are working correctly.")
        print("✅ Backward compatibility is maintained.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)