/********************************************************************************
** Form generated from reading UI file 'camera_calibration_data_manager_widget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CAMERA_CALIBRATION_DATA_MANAGER_WIDGET_H
#define UI_CAMERA_CALIBRATION_DATA_MANAGER_WIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_CameraCalibrationDataManager
{
public:
    QVBoxLayout *verticalLayout_2;
    QTabWidget *tab_widget;
    QWidget *tab_observations;
    QVBoxLayout *verticalLayout;
    QFormLayout *formLayout;
    QDoubleSpinBox *double_spin_box_homography_threshold;
    QLabel *label;
    QTreeWidget *tree_widget_observations;
    QWidget *tab_results;
    QVBoxLayout *verticalLayout_3;
    QTextEdit *text_edit_results;

    void setupUi(QWidget *CameraCalibrationDataManager)
    {
        if (CameraCalibrationDataManager->objectName().isEmpty())
            CameraCalibrationDataManager->setObjectName(QString::fromUtf8("CameraCalibrationDataManager"));
        CameraCalibrationDataManager->resize(329, 176);
        verticalLayout_2 = new QVBoxLayout(CameraCalibrationDataManager);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        tab_widget = new QTabWidget(CameraCalibrationDataManager);
        tab_widget->setObjectName(QString::fromUtf8("tab_widget"));
        tab_observations = new QWidget();
        tab_observations->setObjectName(QString::fromUtf8("tab_observations"));
        verticalLayout = new QVBoxLayout(tab_observations);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        formLayout = new QFormLayout();
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        double_spin_box_homography_threshold = new QDoubleSpinBox(tab_observations);
        double_spin_box_homography_threshold->setObjectName(QString::fromUtf8("double_spin_box_homography_threshold"));
        double_spin_box_homography_threshold->setValue(2.000000000000000);

        formLayout->setWidget(0, QFormLayout::LabelRole, double_spin_box_homography_threshold);

        label = new QLabel(tab_observations);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout->setWidget(0, QFormLayout::FieldRole, label);


        verticalLayout->addLayout(formLayout);

        tree_widget_observations = new QTreeWidget(tab_observations);
        tree_widget_observations->setObjectName(QString::fromUtf8("tree_widget_observations"));
        tree_widget_observations->setAlternatingRowColors(true);
        tree_widget_observations->setTextElideMode(Qt::ElideRight);
        tree_widget_observations->setUniformRowHeights(false);
        tree_widget_observations->setAllColumnsShowFocus(true);
        tree_widget_observations->setWordWrap(true);
        tree_widget_observations->header()->setVisible(true);

        verticalLayout->addWidget(tree_widget_observations);

        tab_widget->addTab(tab_observations, QString());
        tab_results = new QWidget();
        tab_results->setObjectName(QString::fromUtf8("tab_results"));
        verticalLayout_3 = new QVBoxLayout(tab_results);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        text_edit_results = new QTextEdit(tab_results);
        text_edit_results->setObjectName(QString::fromUtf8("text_edit_results"));
        text_edit_results->setReadOnly(true);

        verticalLayout_3->addWidget(text_edit_results);

        tab_widget->addTab(tab_results, QString());

        verticalLayout_2->addWidget(tab_widget);


        retranslateUi(CameraCalibrationDataManager);

        tab_widget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(CameraCalibrationDataManager);
    } // setupUi

    void retranslateUi(QWidget *CameraCalibrationDataManager)
    {
        CameraCalibrationDataManager->setWindowTitle(QCoreApplication::translate("CameraCalibrationDataManager", "Form", nullptr));
        double_spin_box_homography_threshold->setSuffix(QCoreApplication::translate("CameraCalibrationDataManager", " pixels", nullptr));
        label->setText(QCoreApplication::translate("CameraCalibrationDataManager", "Homography Threshold", nullptr));
        QTreeWidgetItem *___qtreewidgetitem = tree_widget_observations->headerItem();
        ___qtreewidgetitem->setText(1, QCoreApplication::translate("CameraCalibrationDataManager", "Notes", nullptr));
        ___qtreewidgetitem->setText(0, QCoreApplication::translate("CameraCalibrationDataManager", "Observation", nullptr));
        tab_widget->setTabText(tab_widget->indexOf(tab_observations), QCoreApplication::translate("CameraCalibrationDataManager", "Observations", nullptr));
        tab_widget->setTabText(tab_widget->indexOf(tab_results), QCoreApplication::translate("CameraCalibrationDataManager", "Results", nullptr));
    } // retranslateUi

};

namespace Ui {
    class CameraCalibrationDataManager: public Ui_CameraCalibrationDataManager {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CAMERA_CALIBRATION_DATA_MANAGER_WIDGET_H
