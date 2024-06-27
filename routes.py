from flask import Blueprint, render_template, request, redirect, url_for
from .models import Listing, Review
from .utils import wrap_async, validate_review

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("listings/login.html")

@main.route("/listings")
def listings():
    all_listings = Listing.objects()
    return render_template("listings/index.html", all_listings=all_listings)

@main.route("/listings/new", methods=["GET", "POST"])
def new_listing():
    if request.method == "POST":
        new_listing = Listing(
            title=request.form.get("title"),
            description=request.form.get("description"),
            image=request.form.get("image"),
            writer=request.form.get("writer"),
            price=int(request.form.get("price"))
        )
        new_listing.save()
        return redirect(url_for("main.listings"))
    return render_template("listings/new.html")

@main.route("/listings/<id>")
def show_listing(id):
    listing = Listing.objects(id=id).first()
    return render_template("listings/show.html", listing=listing)

@main.route("/listings/<id>/edit", methods=["GET", "POST"])
def edit_listing(id):
    listing = Listing.objects(id=id).first()
    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.description = request.form.get("description")
        listing.image = request.form.get("image")
        listing.writer = request.form.get("writer")
        listing.price = int(request.form.get("price"))
        listing.save()
        return redirect(url_for("main.listings"))
    return render_template("listings/edit.html", listing=listing)

@main.route("/listings/<id>/delete", methods=["POST"])
def delete_listing(id):
    listing = Listing.objects(id=id).first()
    if listing:
        listing.delete()
    return redirect(url_for("main.listings"))

@main.route("/listings/<id>/reviews", methods=["POST"])
@wrap_async
async def add_review(id):
    listing = Listing.objects(id=id).first()
    new_review = Review(
        content=request.form.get("content"),
        rating=int(request.form.get("rating")),
        listing=listing
    )
    await new_review.save()
    listing.reviews.append(new_review)
    await listing.save()
    return redirect(url_for("main.show_listing", id=id))

@main.route("/listings/<id>/reviews/<review_id>/delete", methods=["POST"])
@wrap_async
async def delete_review(id, review_id):
    await Review.objects(id=review_id).delete()
    await Listing.objects(id=id).update_one(pull__reviews=review_id)
    return redirect(url_for("main.show_listing", id=id))

@main.route("/recommend")
def recommend():
    return render_template("listings/recommends.html")

@main.route("/signUp")
def sign_up():
    return render_template("listings/signup.html")

# Error handling
@main.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page Not Found"), 404

@main.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Internal Server Error"), 500
