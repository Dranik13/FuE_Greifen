/********************************************************************************
** Form generated from reading UI file 'transform_guess.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TRANSFORM_GUESS_H
#define UI_TRANSFORM_GUESS_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TransformGuess
{
public:
    QFormLayout *formLayout;
    QLabel *label_6;
    QDoubleSpinBox *double_spin_box_x;
    QLabel *label;
    QDoubleSpinBox *double_spin_box_y;
    QLabel *label_2;
    QDoubleSpinBox *double_spin_box_z;
    QLabel *label_3;
    QDoubleSpinBox *double_spin_box_qx;
    QLabel *label_4;
    QDoubleSpinBox *double_spin_box_qy;
    QLabel *label_5;
    QDoubleSpinBox *double_spin_box_qz;
    QLabel *label_7;
    QDoubleSpinBox *double_spin_box_qw;

    void setupUi(QWidget *TransformGuess)
    {
        if (TransformGuess->objectName().isEmpty())
            TransformGuess->setObjectName(QString::fromUtf8("TransformGuess"));
        TransformGuess->resize(235, 236);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(TransformGuess->sizePolicy().hasHeightForWidth());
        TransformGuess->setSizePolicy(sizePolicy);
        formLayout = new QFormLayout(TransformGuess);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        label_6 = new QLabel(TransformGuess);
        label_6->setObjectName(QString::fromUtf8("label_6"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label_6);

        double_spin_box_x = new QDoubleSpinBox(TransformGuess);
        double_spin_box_x->setObjectName(QString::fromUtf8("double_spin_box_x"));
        double_spin_box_x->setDecimals(6);
        double_spin_box_x->setMinimum(-1000000000.000000000000000);
        double_spin_box_x->setMaximum(1000000000.000000000000000);
        double_spin_box_x->setSingleStep(0.010000000000000);

        formLayout->setWidget(0, QFormLayout::FieldRole, double_spin_box_x);

        label = new QLabel(TransformGuess);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label);

        double_spin_box_y = new QDoubleSpinBox(TransformGuess);
        double_spin_box_y->setObjectName(QString::fromUtf8("double_spin_box_y"));
        double_spin_box_y->setDecimals(6);
        double_spin_box_y->setMinimum(-1000000000.000000000000000);
        double_spin_box_y->setMaximum(1000000000.000000000000000);
        double_spin_box_y->setSingleStep(0.010000000000000);

        formLayout->setWidget(1, QFormLayout::FieldRole, double_spin_box_y);

        label_2 = new QLabel(TransformGuess);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout->setWidget(2, QFormLayout::LabelRole, label_2);

        double_spin_box_z = new QDoubleSpinBox(TransformGuess);
        double_spin_box_z->setObjectName(QString::fromUtf8("double_spin_box_z"));
        double_spin_box_z->setDecimals(6);
        double_spin_box_z->setMinimum(-1000000000.000000000000000);
        double_spin_box_z->setMaximum(1000000000.000000000000000);
        double_spin_box_z->setSingleStep(0.010000000000000);

        formLayout->setWidget(2, QFormLayout::FieldRole, double_spin_box_z);

        label_3 = new QLabel(TransformGuess);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        formLayout->setWidget(3, QFormLayout::LabelRole, label_3);

        double_spin_box_qx = new QDoubleSpinBox(TransformGuess);
        double_spin_box_qx->setObjectName(QString::fromUtf8("double_spin_box_qx"));
        double_spin_box_qx->setDecimals(6);
        double_spin_box_qx->setMinimum(-1.000000000000000);
        double_spin_box_qx->setMaximum(1.000000000000000);
        double_spin_box_qx->setSingleStep(0.010000000000000);

        formLayout->setWidget(3, QFormLayout::FieldRole, double_spin_box_qx);

        label_4 = new QLabel(TransformGuess);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        formLayout->setWidget(4, QFormLayout::LabelRole, label_4);

        double_spin_box_qy = new QDoubleSpinBox(TransformGuess);
        double_spin_box_qy->setObjectName(QString::fromUtf8("double_spin_box_qy"));
        double_spin_box_qy->setDecimals(6);
        double_spin_box_qy->setMinimum(-1.000000000000000);
        double_spin_box_qy->setMaximum(1.000000000000000);
        double_spin_box_qy->setSingleStep(0.010000000000000);

        formLayout->setWidget(4, QFormLayout::FieldRole, double_spin_box_qy);

        label_5 = new QLabel(TransformGuess);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        formLayout->setWidget(5, QFormLayout::LabelRole, label_5);

        double_spin_box_qz = new QDoubleSpinBox(TransformGuess);
        double_spin_box_qz->setObjectName(QString::fromUtf8("double_spin_box_qz"));
        double_spin_box_qz->setDecimals(6);
        double_spin_box_qz->setMinimum(-1.000000000000000);
        double_spin_box_qz->setMaximum(1.000000000000000);
        double_spin_box_qz->setSingleStep(0.010000000000000);

        formLayout->setWidget(5, QFormLayout::FieldRole, double_spin_box_qz);

        label_7 = new QLabel(TransformGuess);
        label_7->setObjectName(QString::fromUtf8("label_7"));

        formLayout->setWidget(6, QFormLayout::LabelRole, label_7);

        double_spin_box_qw = new QDoubleSpinBox(TransformGuess);
        double_spin_box_qw->setObjectName(QString::fromUtf8("double_spin_box_qw"));
        double_spin_box_qw->setDecimals(6);
        double_spin_box_qw->setMinimum(-1.000000000000000);
        double_spin_box_qw->setMaximum(1.000000000000000);
        double_spin_box_qw->setSingleStep(0.010000000000000);
        double_spin_box_qw->setValue(1.000000000000000);

        formLayout->setWidget(6, QFormLayout::FieldRole, double_spin_box_qw);


        retranslateUi(TransformGuess);

        QMetaObject::connectSlotsByName(TransformGuess);
    } // setupUi

    void retranslateUi(QWidget *TransformGuess)
    {
        TransformGuess->setWindowTitle(QCoreApplication::translate("TransformGuess", "Form", nullptr));
        label_6->setText(QCoreApplication::translate("TransformGuess", "x (m)", nullptr));
        label->setText(QCoreApplication::translate("TransformGuess", "y (m)", nullptr));
        label_2->setText(QCoreApplication::translate("TransformGuess", "z (m)", nullptr));
        label_3->setText(QCoreApplication::translate("TransformGuess", "qx", nullptr));
        label_4->setText(QCoreApplication::translate("TransformGuess", "qy", nullptr));
        label_5->setText(QCoreApplication::translate("TransformGuess", "qz", nullptr));
        label_7->setText(QCoreApplication::translate("TransformGuess", "qw", nullptr));
    } // retranslateUi

};

namespace Ui {
    class TransformGuess: public Ui_TransformGuess {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TRANSFORM_GUESS_H
