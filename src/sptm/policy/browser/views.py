# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.app.contenttypes.browser.collection import CollectionView
from sptm.policy.interfaces import IHeadLineView
from sptm.policy.interfaces import IRestView
import requests

curmap = {'research': ((u'活動成果', 'Activity', '/research'), (u'研究成果', 'Research', '/research'), (u'主題成果', 'Project', '/research'))}

class HeadLineView(CollectionView):
    implements(IHeadLineView)

    def __init__(self, *args, **kwargs):
        super(HeadLineView, self).__init__(*args, **kwargs)

    def at_root(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.portal_url()

    def newsitems(self):
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type='News Item',
                       path='mysite/news',
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=3)[:3]

    def cgisitems(self):
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type='Document',
                       path='mysite/cgis',
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=4)[:4]

    def rlgnitems(self):
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type='Document',
                       path='mysite/religion',
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=4)[:4]

    def dstritems(self):
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type='Document',
                       path='mysite/district',
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=4)[:4]

    def cntritems(self):
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type='Document',
                       path='mysite/center',
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=4)[:4]

    def fldrmap(self):
        curfldr = self.context.absolute_url().split('/')[-2]
        if curfldr in curmap:
            return curmap[curfldr]
        else:
            return tuple()

    def fldrpath(self, fldr):
        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        return portal_state.navigation_root_path() + fldr

    def latest(self, ctpfldr):
        if ctpfldr == tuple(): return None
        context = self.context.aq_inner
        catalog = getToolByName(context, 'portal_catalog')
        path = self.fldrpath(ctpfldr[2])
        return catalog(portal_type=ctpfldr[1],
                       path=path,
                       sort_on='created',
                       sort_order='reverse',
                       sort_limit=3)[:3]

class RestView(BrowserView):
    implements(IRestView)

    def getData(self):
        request = self.request
        b_start = request.get('b_start')
        url = 'http://crgis.rchss.sinica.edu.tw/@search?fullobjects&portal_type=News%20Item&b_size=10&b_start={}'.format(b_start)
        data = requests.get(url, headers={'Accept': 'application/json'})
        return data.json()

    def getNext(self):
        request = self.request
        b_start = int(request.get('b_start'))
        return str(b_start + 10)

    def getPrev(self):
        request = self.request
        b_start = int(request.get('b_start'))
        b_start = b_start - 10 if b_start >= 10 else 0
        return str(b_start)

