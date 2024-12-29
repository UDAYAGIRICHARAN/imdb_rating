from django.shortcuts import render
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
import logging
import datetime

@csrf_exempt
def upload_csv(request):
    try:
        if request.method == 'POST' and request.FILES.get('file'):
            csv_file = request.FILES['file']

            if csv_file.size > 100 * 1024 * 1024:  # 100 MB limit
                return JsonResponse({'error': 'File size exceeds 100MB'}, status=400)

            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                movies = []
                for row in reader:
                    release_date = None
                    try:
                        release_date = datetime.datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                    except (ValueError, KeyError):
                        release_date = None

                    movies.append(Movie(
                        title=row['title'],
                        release_date=release_date,
                        language=row['original_language'],
                        rating=float(row['vote_average']) if row['vote_average'] else 0.0,
                        description=row['overview'],
                        budget=float(row['budget']) if row['budget'] else 0.0,
                        revenue=float(row['revenue']) if row['revenue'] else 0.0,
                        runtime=int(row['runtime']) if row['runtime'] else 0,
                        status=row['status']
                    ))
                
                # Bulk create movies, skipping invalid rows
                movies = [movie for movie in movies if movie.release_date is not None]
                Movie.objects.bulk_create(movies)

                return JsonResponse({'message': 'File uploaded successfully'})

            except Exception as e:
                logging.error(f"Error processing file: {e}")
                return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'error': 'Invalid request method or file'}, status=400)

    except Exception as e:
        logging.error(e)
        return JsonResponse({'error': str(e)}, status=500)
def get_movies(request):
    try:
        # Pagination parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # Filtering parameters
        language = request.GET.get('language')
        year = request.GET.get('year')

        # Sorting parameter
        sort_by = request.GET.get('sort_by', 'release_date')  # Default to 'release_date' if not provided

        # Validate the sort_by field
        valid_sort_fields = ['release_date', 'rating']
        if sort_by not in valid_sort_fields:
            return JsonResponse({'error': f"Invalid sort field: '{sort_by}'"}, status=400)

        # Query movies
        movies = Movie.objects.all()

        # Filtering
        if language:
            movies = movies.filter(language__icontains=language)
        if year:
            movies = movies.filter(release_date__year=year)

        # Sorting
        movies = movies.order_by(sort_by)

        # Pagination
        paginator = Paginator(movies, page_size)
        paginated_movies = paginator.get_page(page)

        # Serialize data
        data = [{
            'title': movie.title,
            'release_date': movie.release_date,
            'language': movie.language,
            'rating': movie.rating,
            'description': movie.description,
            'budget': movie.budget,
            'revenue': movie.revenue,
            'runtime': movie.runtime,
            'status': movie.status
        } for movie in paginated_movies]

        return JsonResponse({
            'movies': data,
            'total_pages': paginator.num_pages,
            'current_page': paginated_movies.number,
            'page_size': page_size,
            'total_movies': paginator.count
        })

    except Exception as e:
        logging.error(f"Error in get_movies: {e}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)