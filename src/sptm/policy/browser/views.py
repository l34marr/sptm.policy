from zope.interface import implements
from plone.app.contenttypes.browser.collection import CollectionView
from sptm.policy.interfaces import IHeadLineView


class HeadLineView(CollectionView):
    implements(IHeadLineView)

