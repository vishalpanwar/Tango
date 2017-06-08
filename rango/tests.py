from django.test import TestCase
from rango.models import Category
from django.core.urlresolvers import reverse

# Create your tests here.

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        cat = Category(name = 'test',views = 1,likes= 0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name = "Random Category String")
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

def add_cat(name,views = 0,likes = 0):
    c = Category.objects.get_or_create(name = name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class IndexViewTests(TestCase):

    def test_index_view_with_category(self):

        add_cat('test')
        add_cat('temp')
        add_cat('tmp test temp')
        add_cat('tmp')

        response = self.client.get(reverse('rango_index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'tmp test temp')
        num_cats = len(response.context['categories'])
        self.assertEquals(num_cats,4)

    def test_index_view_with_no_category(self):

        response = self.client.get(reverse('rango_index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'There are no categories present.')
        num_cats = len(response.context['categories'])
        self.assertEquals(num_cats,0)


class LoginTests(TestCase):

    '''
        <<<<<<<<<<<<<<ToDO>>>>>>>>>>>>>>>>
    '''
    def test_login_view_user_already_present(self):

        response = self.client.get(reverse('rango_user_login'))
        print('>>>>>>>>>>>>>>>>>>>>>>',response)