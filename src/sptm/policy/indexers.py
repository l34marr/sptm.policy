#!/usr/bin/python
# -*- coding: utf-8 -*-

from Acquisition import aq_base
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.indexer.decorator import indexer
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.app.contenttypes.indexers import SearchableText
from Products.CMFPlone.utils import safe_unicode
from sptm.content.interfaces import IActivity
from sptm.content.interfaces import IResearch
from sptm.content.interfaces import IProject


@indexer(IActivity)
def ctgr_activity(obj, **kw):
    return obj.a_ctgr

@indexer(IResearch)
def ctgr_research(obj, **kw):
    return obj.r_ctgr

@indexer(IProject)
def ctgr_project(obj, **kw):
    return obj.p_ctgr

