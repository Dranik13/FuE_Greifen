/********************************************************************************
** Form generated from reading UI file 'target_finder.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TARGET_FINDER_H
#define UI_TARGET_FINDER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TargetFinder
{
public:
    QVBoxLayout *verticalLayout;
    QGroupBox *group_box;
    QVBoxLayout *verticalLayout_2;
    QComboBox *combo_box_target_finder;
    QFrame *line;
    QStackedWidget *stacked_widget;

    void setupUi(QWidget *TargetFinder)
    {
        if (TargetFinder->objectName().isEmpty())
            TargetFinder->setObjectName(QString::fromUtf8("TargetFinder"));
        TargetFinder->resize(435, 131);
        verticalLayout = new QVBoxLayout(TargetFinder);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        group_box = new QGroupBox(TargetFinder);
        group_box->setObjectName(QString::fromUtf8("group_box"));
        verticalLayout_2 = new QVBoxLayout(group_box);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        combo_box_target_finder = new QComboBox(group_box);
        combo_box_target_finder->setObjectName(QString::fromUtf8("combo_box_target_finder"));

        verticalLayout_2->addWidget(combo_box_target_finder);

        line = new QFrame(group_box);
        line->setObjectName(QString::fromUtf8("line"));
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);

        verticalLayout_2->addWidget(line);

        stacked_widget = new QStackedWidget(group_box);
        stacked_widget->setObjectName(QString::fromUtf8("stacked_widget"));

        verticalLayout_2->addWidget(stacked_widget);


        verticalLayout->addWidget(group_box);


        retranslateUi(TargetFinder);

        QMetaObject::connectSlotsByName(TargetFinder);
    } // setupUi

    void retranslateUi(QWidget *TargetFinder)
    {
        TargetFinder->setWindowTitle(QCoreApplication::translate("TargetFinder", "Form", nullptr));
        group_box->setTitle(QCoreApplication::translate("TargetFinder", "Target Finder", nullptr));
    } // retranslateUi

};

namespace Ui {
    class TargetFinder: public Ui_TargetFinder {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TARGET_FINDER_H
