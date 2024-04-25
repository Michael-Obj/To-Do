from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import ToDo

# Create your views here.


def Search(request):
    try:
        # query = request.GET.get('example-search-input')
        query = request.POST['search_value']
        username = request.session["username"]
        userId = request.session["userId"]
        results = ""
        
        if query:
            results = ToDo.objects.filter(input_field__icontains=query, user_id=userId)
            return render(request, "index.html", {"todoLists": results, "username": username, "query":query})
    
    except Exception as ex:
            print(ex)


    
def Sort(request, sort_param):
    try:
        username = request.session["username"]
        userId = request.session["userId"]

        if sort_param=="alphabet":
            results = ToDo.objects.filter(user_id=userId).order_by('input_field')
            return render(request, "index.html", {"todoLists": results, "username": username})
        
        elif sort_param=="date":
            results = ToDo.objects.filter(user_id=userId).order_by('-date_created')
            return render(request, "index.html", {"todoLists": results, "username": username})

    except Exception as ex:
            print(ex)




def Home(request):
    session_keys = list(request.session.keys())
    if len(session_keys) != 0:
        try:
            username = request.session["username"]
            userId = request.session["userId"]
            # session_keys = list(request.session.keys())
            todoAll = ToDo.objects.filter(user_id = userId).order_by('-date_created').values()
            return render(request, "index.html", {"todoLists": todoAll, "username": username})

        except Exception as ex:
            print(ex)
    return redirect("loginUser")


def CreateToDo(request):
    session_keys = list(request.session.keys())
    if len(session_keys) != 0:
        try:
            if request.method=='POST':
                input_field = request.POST['input_field']

                if len(input_field) != 0:
                    user_id = request.session["userId"]
                    user_obj = User.objects.get(pk = user_id)
                    
                    todo = ToDo(
                        input_field=input_field,
                        user=user_obj
                        )
                    todo.save()
                    # print('todo created')
                    messages.success(request, 'Success! New Item Added')
                    return redirect("home")
                return redirect("home")

            else:
                return render(request, "create.html")

        except Exception as ex:
            print(ex)
    return redirect("loginUser")



def GetByIdToDo(request, id):
    try:
        todoById = ToDo.objects.get(pk = id)
        return render(request, "update.html", {"todo": todoById}) 

    except Exception as ex:
        print(ex)



def UpdateToDo(request, id):
    try:
        if request.method=='POST':
            input_field = request.POST['input_field']

            if len(input_field) != 0:
                todoUpdate = ToDo.objects.get(pk = id)
                todoUpdate.input_field = input_field

                todoUpdate.save()
                messages.success(request, 'Success! Item Updated')
                return redirect("home")
            return redirect("home")
        
        else:
            return render(request, "update.html")  

    except Exception as ex:
        print(ex)



def DeleteToDo(request, id):
    try:
        todoDelete = ToDo.objects.get(pk = id).delete()

        messages.error(request, 'Item Deleted')
        return redirect("home")  

    except Exception as ex:
        print(ex)





#account

def RegisterUser(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password==confirm_password:                                
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username taken')
                    return redirect("registerUser")  
                
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,  
                        password=password
                        )
                    user.save()
                    return render(request, "login.html")  
                
            else:
                messages.error(request, 'Password not the same')
                return redirect("registerUser")  
            
        else: 
            return render(request, "register.html") 

    except Exception as ex:
        print(ex)




def LoginUser(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                request.session["userId"] = user.id
                request.session["username"] = user.username

                return redirect("home")  

            else:
                messages.error(request, 'Incorrect username or password')
                return render(request, "login.html")
            
        elif request.method=='GET':
            return render(request, "login.html")

            
    except Exception as ex:
        print(ex)



def LogoutUser(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    auth.logout(request)
    return redirect("loginUser")

