/********************************************************************************
** Form generated from reading UI file 'aruco_grid_target_finder.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ARUCO_GRID_TARGET_FINDER_H
#define UI_ARUCO_GRID_TARGET_FINDER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ArucoGridTargetFinder
{
public:
    QFormLayout *formLayout;
    QLabel *label;
    QSpinBox *spin_box_rows;
    QLabel *label_2;
    QSpinBox *spin_box_cols;
    QLabel *label_3;
    QDoubleSpinBox *double_spin_box_marker_size;
    QLabel *label_4;
    QComboBox *combo_box_dict;
    QLabel *label_5;
    QDoubleSpinBox *double_spin_box_marker_gap;

    void setupUi(QWidget *ArucoGridTargetFinder)
    {
        if (ArucoGridTargetFinder->objectName().isEmpty())
            ArucoGridTargetFinder->setObjectName(QString::fromUtf8("ArucoGridTargetFinder"));
        ArucoGridTargetFinder->resize(324, 171);
        formLayout = new QFormLayout(ArucoGridTargetFinder);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        label = new QLabel(ArucoGridTargetFinder);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label);

        spin_box_rows = new QSpinBox(ArucoGridTargetFinder);
        spin_box_rows->setObjectName(QString::fromUtf8("spin_box_rows"));
        spin_box_rows->setMinimum(1);

        formLayout->setWidget(0, QFormLayout::FieldRole, spin_box_rows);

        label_2 = new QLabel(ArucoGridTargetFinder);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label_2);

        spin_box_cols = new QSpinBox(ArucoGridTargetFinder);
        spin_box_cols->setObjectName(QString::fromUtf8("spin_box_cols"));
        spin_box_cols->setMinimum(1);

        formLayout->setWidget(1, QFormLayout::FieldRole, spin_box_cols);

        label_3 = new QLabel(ArucoGridTargetFinder);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        formLayout->setWidget(2, QFormLayout::LabelRole, label_3);

        double_spin_box_marker_size = new QDoubleSpinBox(ArucoGridTargetFinder);
        double_spin_box_marker_size->setObjectName(QString::fromUtf8("double_spin_box_marker_size"));
        double_spin_box_marker_size->setDecimals(6);
        double_spin_box_marker_size->setSingleStep(0.010000000000000);
        double_spin_box_marker_size->setValue(0.010000000000000);

        formLayout->setWidget(2, QFormLayout::FieldRole, double_spin_box_marker_size);

        label_4 = new QLabel(ArucoGridTargetFinder);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        formLayout->setWidget(4, QFormLayout::LabelRole, label_4);

        combo_box_dict = new QComboBox(ArucoGridTargetFinder);
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->addItem(QString());
        combo_box_dict->setObjectName(QString::fromUtf8("combo_box_dict"));

        formLayout->setWidget(4, QFormLayout::FieldRole, combo_box_dict);

        label_5 = new QLabel(ArucoGridTargetFinder);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        formLayout->setWidget(3, QFormLayout::LabelRole, label_5);

        double_spin_box_marker_gap = new QDoubleSpinBox(ArucoGridTargetFinder);
        double_spin_box_marker_gap->setObjectName(QString::fromUtf8("double_spin_box_marker_gap"));
        double_spin_box_marker_gap->setDecimals(6);
        double_spin_box_marker_gap->setSingleStep(0.010000000000000);
        double_spin_box_marker_gap->setValue(0.005000000000000);

        formLayout->setWidget(3, QFormLayout::FieldRole, double_spin_box_marker_gap);

        QWidget::setTabOrder(spin_box_rows, spin_box_cols);
        QWidget::setTabOrder(spin_box_cols, double_spin_box_marker_size);
        QWidget::setTabOrder(double_spin_box_marker_size, double_spin_box_marker_gap);
        QWidget::setTabOrder(double_spin_box_marker_gap, combo_box_dict);

        retranslateUi(ArucoGridTargetFinder);

        QMetaObject::connectSlotsByName(ArucoGridTargetFinder);
    } // setupUi

    void retranslateUi(QWidget *ArucoGridTargetFinder)
    {
        ArucoGridTargetFinder->setWindowTitle(QCoreApplication::translate("ArucoGridTargetFinder", "Form", nullptr));
        label->setText(QCoreApplication::translate("ArucoGridTargetFinder", "Rows", nullptr));
        label_2->setText(QCoreApplication::translate("ArucoGridTargetFinder", "Columns", nullptr));
        label_3->setText(QCoreApplication::translate("ArucoGridTargetFinder", "Marker Size (m)", nullptr));
        label_4->setText(QCoreApplication::translate("ArucoGridTargetFinder", "Dictionary", nullptr));
        combo_box_dict->setItemText(0, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_4X4_50", nullptr));
        combo_box_dict->setItemText(1, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_4X4_100", nullptr));
        combo_box_dict->setItemText(2, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_4X4_250", nullptr));
        combo_box_dict->setItemText(3, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_4X4_1000", nullptr));
        combo_box_dict->setItemText(4, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_5X5_50", nullptr));
        combo_box_dict->setItemText(5, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_5X5_100", nullptr));
        combo_box_dict->setItemText(6, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_5X5_250", nullptr));
        combo_box_dict->setItemText(7, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_5X5_1000", nullptr));
        combo_box_dict->setItemText(8, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_6X6_50", nullptr));
        combo_box_dict->setItemText(9, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_6X6_100", nullptr));
        combo_box_dict->setItemText(10, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_6X6_250", nullptr));
        combo_box_dict->setItemText(11, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_6X6_1000", nullptr));
        combo_box_dict->setItemText(12, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_7X7_50", nullptr));
        combo_box_dict->setItemText(13, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_7X7_250", nullptr));
        combo_box_dict->setItemText(14, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_7X7_1000", nullptr));
        combo_box_dict->setItemText(15, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_ARUCO_ORIGINAL", nullptr));
        combo_box_dict->setItemText(16, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_APRILTAG_16h5", nullptr));
        combo_box_dict->setItemText(17, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_APRILTAG_25h9", nullptr));
        combo_box_dict->setItemText(18, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_APRILTAG_36h10", nullptr));
        combo_box_dict->setItemText(19, QCoreApplication::translate("ArucoGridTargetFinder", "DICT_APRILTAG_36h11", nullptr));

        label_5->setText(QCoreApplication::translate("ArucoGridTargetFinder", "Marker Gap (m)", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ArucoGridTargetFinder: public Ui_ArucoGridTargetFinder {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ARUCO_GRID_TARGET_FINDER_H
