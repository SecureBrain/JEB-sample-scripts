# JEB sample script
# http://www.android-decompiler.com/
#
# RenameObfuscatedClasses.py
# Rename obfuscated class names.
#
# Copyright (c) 2013 SecureBrain
import re

from jeb.api import IScript
from jeb.api import EngineOption
from jeb.api.ui import JebUI
from jeb.api.ui import View

class RenameObfuscatedClasses(IScript):
    def run(self, j):
        self.dex = j.getDex()
        self.jeb = j
        ui = j.getUI()

        # rename obfuscated class name
        self.rename_classes()

        # refresh view
        ui.getView(View.Type.ASSEMBLY).refresh()
        ui.getView(View.Type.JAVA).refresh()

    def rename_classes(self):
        rename_targets = {
            'Landroid/app/Service;': 'Service',
            'Landroid/app/Activity;': 'Activity',
            'Landroid/content/BroadcastReceiver;': 'Receiver',
            'Landroid/content/ContentProvider;': 'Provider',
            'Ljava/lang/Thread;': 'Thread',
            'Landroid/os/AsyncTask;': 'AsyncTask',
            'Landroid/database/sqlite/SQLiteDatabase;': 'SQLiteDatabase',
            'Landroid/database/sqlite/SQLiteOpenHelper;': 'SQLiteOpenHelper',
        }
        for i in range(0, self.dex.getClassCount()):
            cls = self.dex.getClass(i)
            cls_name = self.dex.getType(cls.getClasstypeIndex())
            super_cls_name = self.dex.getType(cls.getSuperclassIndex())
            p = re.compile("^.*\/([\w$]+);$")
            if super_cls_name in rename_targets.keys():
                val = rename_targets[super_cls_name]
                if not cls_name.endswith(val + ';'):
                    s = re.search(p, cls_name)
                    simple_new_name = s.group(1) + '_' + val
                    ret = self.jeb.renameClass(cls_name, simple_new_name)
                    print "rename from '%s' to '%s'" % (cls_name, simple_new_name)


