/********************************************************************************
** Form generated from reading UI file 'charuco_grid_target_finder.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CHARUCO_GRID_TARGET_FINDER_H
#define UI_CHARUCO_GRID_TARGET_FINDER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_CharucoGridTargetFinder
{
public:
    QFormLayout *formLayout;
    QLabel *label;
    QSpinBox *rowSpinBox;
    QLabel *label_2;
    QSpinBox *colSpinBox;
    QLabel *label_3;
    QDoubleSpinBox *checkerSizeDoubleSpinBox;
    QLabel *label_4;
    QDoubleSpinBox *markerSizeDoubleSpinBox;
    QLabel *label_5;
    QComboBox *dictComboBox;

    void setupUi(QWidget *CharucoGridTargetFinder)
    {
        if (CharucoGridTargetFinder->objectName().isEmpty())
            CharucoGridTargetFinder->setObjectName(QString::fromUtf8("CharucoGridTargetFinder"));
        CharucoGridTargetFinder->resize(330, 182);
        formLayout = new QFormLayout(CharucoGridTargetFinder);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        label = new QLabel(CharucoGridTargetFinder);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label);

        rowSpinBox = new QSpinBox(CharucoGridTargetFinder);
        rowSpinBox->setObjectName(QString::fromUtf8("rowSpinBox"));
        rowSpinBox->setMinimum(2);

        formLayout->setWidget(0, QFormLayout::FieldRole, rowSpinBox);

        label_2 = new QLabel(CharucoGridTargetFinder);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label_2);

        colSpinBox = new QSpinBox(CharucoGridTargetFinder);
        colSpinBox->setObjectName(QString::fromUtf8("colSpinBox"));
        colSpinBox->setMinimum(2);

        formLayout->setWidget(1, QFormLayout::FieldRole, colSpinBox);

        label_3 = new QLabel(CharucoGridTargetFinder);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(label_3->sizePolicy().hasHeightForWidth());
        label_3->setSizePolicy(sizePolicy);

        formLayout->setWidget(2, QFormLayout::LabelRole, label_3);

        checkerSizeDoubleSpinBox = new QDoubleSpinBox(CharucoGridTargetFinder);
        checkerSizeDoubleSpinBox->setObjectName(QString::fromUtf8("checkerSizeDoubleSpinBox"));
        checkerSizeDoubleSpinBox->setDecimals(6);
        checkerSizeDoubleSpinBox->setSingleStep(0.010000000000000);
        checkerSizeDoubleSpinBox->setValue(0.020000000000000);

        formLayout->setWidget(2, QFormLayout::FieldRole, checkerSizeDoubleSpinBox);

        label_4 = new QLabel(CharucoGridTargetFinder);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        sizePolicy.setHeightForWidth(label_4->sizePolicy().hasHeightForWidth());
        label_4->setSizePolicy(sizePolicy);

        formLayout->setWidget(3, QFormLayout::LabelRole, label_4);

        markerSizeDoubleSpinBox = new QDoubleSpinBox(CharucoGridTargetFinder);
        markerSizeDoubleSpinBox->setObjectName(QString::fromUtf8("markerSizeDoubleSpinBox"));
        markerSizeDoubleSpinBox->setDecimals(6);
        markerSizeDoubleSpinBox->setSingleStep(0.010000000000000);
        markerSizeDoubleSpinBox->setValue(0.010000000000000);

        formLayout->setWidget(3, QFormLayout::FieldRole, markerSizeDoubleSpinBox);

        label_5 = new QLabel(CharucoGridTargetFinder);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        formLayout->setWidget(4, QFormLayout::LabelRole, label_5);

        dictComboBox = new QComboBox(CharucoGridTargetFinder);
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->addItem(QString());
        dictComboBox->setObjectName(QString::fromUtf8("dictComboBox"));

        formLayout->setWidget(4, QFormLayout::FieldRole, dictComboBox);


        retranslateUi(CharucoGridTargetFinder);

        QMetaObject::connectSlotsByName(CharucoGridTargetFinder);
    } // setupUi

    void retranslateUi(QWidget *CharucoGridTargetFinder)
    {
        CharucoGridTargetFinder->setWindowTitle(QCoreApplication::translate("CharucoGridTargetFinder", "Form", nullptr));
        label->setText(QCoreApplication::translate("CharucoGridTargetFinder", "Rows", nullptr));
        label_2->setText(QCoreApplication::translate("CharucoGridTargetFinder", "Columns", nullptr));
        label_3->setText(QCoreApplication::translate("CharucoGridTargetFinder", "Checker Size (m)", nullptr));
        label_4->setText(QCoreApplication::translate("CharucoGridTargetFinder", "Marker Size (m)", nullptr));
        label_5->setText(QCoreApplication::translate("CharucoGridTargetFinder", "Dictionary", nullptr));
        dictComboBox->setItemText(0, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_4X4_50", nullptr));
        dictComboBox->setItemText(1, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_4X4_100", nullptr));
        dictComboBox->setItemText(2, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_4X4_250", nullptr));
        dictComboBox->setItemText(3, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_4X4_1000", nullptr));
        dictComboBox->setItemText(4, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_5X5_50", nullptr));
        dictComboBox->setItemText(5, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_5X5_100", nullptr));
        dictComboBox->setItemText(6, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_5X5_250", nullptr));
        dictComboBox->setItemText(7, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_5x5_1000", nullptr));
        dictComboBox->setItemText(8, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_6X6_50", nullptr));
        dictComboBox->setItemText(9, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_6X6_100", nullptr));
        dictComboBox->setItemText(10, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_6X6_250", nullptr));
        dictComboBox->setItemText(11, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_6X6_1000", nullptr));
        dictComboBox->setItemText(12, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_7X7_50", nullptr));
        dictComboBox->setItemText(13, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_7X7_100", nullptr));
        dictComboBox->setItemText(14, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_7X7_250", nullptr));
        dictComboBox->setItemText(15, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_7X7_1000", nullptr));
        dictComboBox->setItemText(16, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_ARUCO_ORIGINAL", nullptr));
        dictComboBox->setItemText(17, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_APRILTAG_16h5", nullptr));
        dictComboBox->setItemText(18, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_APRILTAG_25h9", nullptr));
        dictComboBox->setItemText(19, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_APRILTAG_36h10", nullptr));
        dictComboBox->setItemText(20, QCoreApplication::translate("CharucoGridTargetFinder", "DICT_APRILTAG_36h11", nullptr));

    } // retranslateUi

};

namespace Ui {
    class CharucoGridTargetFinder: public Ui_CharucoGridTargetFinder {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CHARUCO_GRID_TARGET_FINDER_H
