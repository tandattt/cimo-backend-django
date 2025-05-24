from django.shortcuts import render
from rest_framework.views import APIView
from Blogs.models import SoBlogs
from Blogs.serializers import SoBlogsSerializer
from rest_framework.response import Response
from rest_framework import status


class SoBlogsView(APIView):
    def get(self, request):
        soBlogs = SoBlogs.objects.order_by('?')[:5]
        serializer = SoBlogsSerializer(soBlogs, many=True)
        response = []
        for i in range(len(serializer.data)):
            imgs = serializer.data[i]['imgs']
            img = imgs.split(',') if imgs else []
            img = [i.strip().strip('"') for i in img]
            print(img)
            response.append({
                'id': serializer.data[i]['id'],
                'name': serializer.data[i]['name'],
                'sumary': serializer.data[i]['sumary'],
                'imgs': img,
                'createdDate': serializer.data[i]['createdDate'],
            })
        return Response(response)
class Get_detail_Blogs(APIView):
    def get(self, request, id):
        soBlogs = SoBlogs.objects.filter(id=id)
        serializer = SoBlogsSerializer(soBlogs, many=True)
        # response = []
        for i in range(len(serializer.data)):
            imgs = serializer.data[i]['imgs']
            img = imgs.split(',') if imgs else []
            img = [i.strip().strip('"') for i in img]
            serializer.data[i]['imgs'] = img
            
        # response.append({serializer.data[i]})
        return Response(serializer.data)
    
class Get_Blog_Filter(APIView):
    def get(self, request):
        skip = request.query_params.get('skip', 0)
        limit = request.query_params.get('limit', 10)

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            return Response({'error': 'skip và limit phải là số nguyên'}, status=status.HTTP_400_BAD_REQUEST)

        blogs = SoBlogs.objects.all()[skip:skip+limit]
        data = []

        for blog in blogs:
            imgs = blog.imgs.split(',') if blog.imgs else []
            imgs = [img.strip().strip('"') for img in imgs]

            data.append({
                'id': blog.id,
                'name': blog.name,
                'sumary': blog.sumary,
                'imgs': imgs,
                'createdDate': blog.createdDate,
            })

        return Response(data, status=status.HTTP_200_OK)