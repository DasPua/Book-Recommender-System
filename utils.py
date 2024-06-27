from functools import wraps
from flask import jsonify, request

def wrap_async(func):
    @wraps(func)
    def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return async_wrapper

def validate_review(req, res, next):
    content = req.form.get("content")
    rating = req.form.get("rating")
    if not content or not rating:
        return res.status(400).json({"error": "Content and Rating are required"})
    next()
