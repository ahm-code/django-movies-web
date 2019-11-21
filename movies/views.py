from django.shortcuts import render
from django.shortcuts import redirect    #needed for redirect to work in create function
from django.contrib import messages      #needed for notification to work when create, delete, update function
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):            # is running when visit myapp.com/create
    #print("haha")
     if request.method == 'POST':   #POST should be capital
         data ={
             'Name': request.POST.get('name'),
             "Pictures":[{
                 "url": request.POST.get("url") or 'https://wingslax.com/wp-content/uploads/2017/12/no-image-available.png'}],   # if url is empty python use the url we gave
             'Rating': int(request.POST.get('rating')),
             'Notes': request.POST.get('notes')
             
             }
         try:
             response = AT.insert(data)   # airtable return a dictionary to us when inserting data
             # notify on create
             messages.success(request, 'New Movie added: {}'.format(response['fields'].get('Name'))) # .get('Name') is replacing ['Name'] so we don't get error when no Name exist
         except Exception as e:
             messages.warning(request, 'Got an error when trying to update a movie: {}'.format(e))
         

     return redirect('/')   #take me to home page

def edit(request, movie_id):
     if request.method == 'POST':   #POST should be capital
         data ={
             'Name': request.POST.get('name'),
             "Pictures":[{
                 "url": request.POST.get("url") or 'https://wingslax.com/wp-content/uploads/2017/12/no-image-available.png'}],
             'Rating': int(request.POST.get('rating')),
             'Notes': request.POST.get('notes')       
             }
         try:
                 response = AT.update(movie_id, data)
                  # notify on edit
                 messages.success(request, 'Updated movie: {}'.format(response['fields'].get('Name')))
         except Exception as e:
                messages.warning(request, 'Got an error when trying to update a movie: {}'.format(e))

     return redirect('/')

def delete(request, movie_id):
     try:
        movie_name = AT.get(movie_id)['fields']['Name']
    
        response = AT.delete(movie_id)
        # notify on delete
        messages.warning(request, 'Movie deleted: {}'.format(movie_name))
     except Exception as e:
                messages.warning(request, 'Got an error when trying to delete a movie: {}'.format(e))
     return redirect('/')