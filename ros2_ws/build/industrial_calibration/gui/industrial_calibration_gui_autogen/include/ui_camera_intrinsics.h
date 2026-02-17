/********************************************************************************
** Form generated from reading UI file 'camera_intrinsics.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CAMERA_INTRINSICS_H
#define UI_CAMERA_INTRINSICS_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_CameraIntrinsics
{
public:
    QFormLayout *formLayout_2;
    QLabel *label;
    QDoubleSpinBox *double_spin_box_fx;
    QLabel *label_2;
    QDoubleSpinBox *double_spin_box_fy;
    QLabel *label_3;
    QDoubleSpinBox *double_spin_box_cx;
    QLabel *label_4;
    QDoubleSpinBox *double_spin_box_cy;

    void setupUi(QWidget *CameraIntrinsics)
    {
        if (CameraIntrinsics->objectName().isEmpty())
            CameraIntrinsics->setObjectName(QString::fromUtf8("CameraIntrinsics"));
        CameraIntrinsics->resize(189, 141);
        formLayout_2 = new QFormLayout(CameraIntrinsics);
        formLayout_2->setObjectName(QString::fromUtf8("formLayout_2"));
        label = new QLabel(CameraIntrinsics);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout_2->setWidget(0, QFormLayout::LabelRole, label);

        double_spin_box_fx = new QDoubleSpinBox(CameraIntrinsics);
        double_spin_box_fx->setObjectName(QString::fromUtf8("double_spin_box_fx"));
        double_spin_box_fx->setDecimals(6);
        double_spin_box_fx->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(0, QFormLayout::FieldRole, double_spin_box_fx);

        label_2 = new QLabel(CameraIntrinsics);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout_2->setWidget(1, QFormLayout::LabelRole, label_2);

        double_spin_box_fy = new QDoubleSpinBox(CameraIntrinsics);
        double_spin_box_fy->setObjectName(QString::fromUtf8("double_spin_box_fy"));
        double_spin_box_fy->setDecimals(6);
        double_spin_box_fy->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(1, QFormLayout::FieldRole, double_spin_box_fy);

        label_3 = new QLabel(CameraIntrinsics);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        formLayout_2->setWidget(2, QFormLayout::LabelRole, label_3);

        double_spin_box_cx = new QDoubleSpinBox(CameraIntrinsics);
        double_spin_box_cx->setObjectName(QString::fromUtf8("double_spin_box_cx"));
        double_spin_box_cx->setDecimals(6);
        double_spin_box_cx->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(2, QFormLayout::FieldRole, double_spin_box_cx);

        label_4 = new QLabel(CameraIntrinsics);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        formLayout_2->setWidget(3, QFormLayout::LabelRole, label_4);

        double_spin_box_cy = new QDoubleSpinBox(CameraIntrinsics);
        double_spin_box_cy->setObjectName(QString::fromUtf8("double_spin_box_cy"));
        double_spin_box_cy->setDecimals(6);
        double_spin_box_cy->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(3, QFormLayout::FieldRole, double_spin_box_cy);


        retranslateUi(CameraIntrinsics);

        QMetaObject::connectSlotsByName(CameraIntrinsics);
    } // setupUi

    void retranslateUi(QWidget *CameraIntrinsics)
    {
        CameraIntrinsics->setWindowTitle(QCoreApplication::translate("CameraIntrinsics", "Form", nullptr));
        label->setText(QCoreApplication::translate("CameraIntrinsics", "fx", nullptr));
        label_2->setText(QCoreApplication::translate("CameraIntrinsics", "fy", nullptr));
        label_3->setText(QCoreApplication::translate("CameraIntrinsics", "cx", nullptr));
        label_4->setText(QCoreApplication::translate("CameraIntrinsics", "cy", nullptr));
    } // retranslateUi

};

namespace Ui {
    class CameraIntrinsics: public Ui_CameraIntrinsics {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CAMERA_INTRINSICS_H
