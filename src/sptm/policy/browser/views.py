# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.app.contenttypes.browser.collection import CollectionView
from sptm.policy.interfaces import IHeadLineView


curmap = {'research': ((u'活動成果', 'Activity', '/research'), (u'研究成果', 'Research', '/research'), (u'主題成果', 'Project', '/research'))}

class HeadLineView(CollectionView):
    implements(IHeadLineView)

    def __init__(self, *args, **kwargs):
        super(HeadLineView, self).__init__(*args, **kwargs)

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

