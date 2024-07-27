"""Exceptions for Vlaams Verkeerscentrum."""


class VerkeersCentrumApiException(Exception):
    """Base exception for Verkeerscentrum API."""


class InvalidCredentialsException(VerkeersCentrumApiException):
    """Invalid credentials exception."""
