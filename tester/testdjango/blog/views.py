from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from blog import models
from django.http import JsonResponse, HttpResponse

# Create your views here.

@require_http_methods(['POST'])
def post_blog(request):
    """
    Create a new blog post.

    :param title:   Title of the blog post
    :param content: Content of the blog post
    :param user_id: ID of the author
    :return code:
    0: success, post created successfully
    1: article already exists
    2: invalid parameter
    3: internal server error
    """

    title = request.POST.get('title')
    content = request.POST.get('content')
    user_id = request.POST.get('user_id')

    response = {}

    required_params = {
        "title":title,
        "content":content,
        "user_id":user_id
    }
    
    # veriify if required values provided
    for param,value in required_params.items():
        if not value:
            response['code']=2
            response['Msg'] = f"Please provide mandatory value {param}"
            return JsonResponse(response,status=400)
    
    # verfiy type of user_id
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        response['code'] = 2
        response['Msg']  = 'user_id must be a valid integer.'
        return JsonResponse(response, status=400)
    
    # verfiy length of title
    if len(title) > 50:
        response['code'] = 2
        response['Msg']  = 'Title cannot exceed 50 characters.'
        return JsonResponse(response, status=400)
    

    try:
        blog_post,created = models.Post.objects.get_or_create(
            title=title,
            user_id = user_id,
            defaults={"content":content}
        )
    except Exception as e:
        response['code']=3
        response['Msg'] = "Internal server error."
        return JsonResponse(response,status=500)
    
    if not created:
        response['code']=1
        response['Msg']= "Article already exists."
        return JsonResponse(response,status=409)
    
    response['code']=0
    response["Msg"] = f"Article {blog_post.title} created successfully."
    return JsonResponse(response,status=200)

