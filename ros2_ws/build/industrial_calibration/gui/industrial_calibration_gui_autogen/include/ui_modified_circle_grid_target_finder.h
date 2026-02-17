/********************************************************************************
** Form generated from reading UI file 'modified_circle_grid_target_finder.ui'
**
** Created by: Qt User Interface Compiler version 5.15.13
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MODIFIED_CIRCLE_GRID_TARGET_FINDER_H
#define UI_MODIFIED_CIRCLE_GRID_TARGET_FINDER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ModifiedCircleGridTargetFinder
{
public:
    QVBoxLayout *verticalLayout_2;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QVBoxLayout *verticalLayout;
    QFrame *frame;
    QFormLayout *formLayout_5;
    QLabel *label;
    QSpinBox *rowSpinBox;
    QLabel *label_2;
    QSpinBox *colSpinBox;
    QLabel *label_3;
    QDoubleSpinBox *spacingDoubleSpinBox;
    QGroupBox *groupBox_5;
    QFormLayout *formLayout_6;
    QLabel *label_8;
    QDoubleSpinBox *circleInclusionRadiusDoubleSpinBox;
    QLabel *label_9;
    QLabel *label_10;
    QDoubleSpinBox *maxRadiusDiffDoubleSpinBox;
    QDoubleSpinBox *maxAvgEllipseErrorDoubleSpinBox;
    QGroupBox *groupBox;
    QFormLayout *formLayout_9;
    QLabel *label_4;
    QSpinBox *minThresholdSpinBox;
    QLabel *label_5;
    QSpinBox *maxThresholdSpinBox;
    QLabel *label_6;
    QSpinBox *numThresholdSpinBox;
    QLabel *label_7;
    QSpinBox *minRepeatSpinBox;
    QCheckBox *filterByColorCheckBox;
    QFrame *frame_filter_color;
    QFormLayout *formLayout_7;
    QLabel *label_12;
    QSpinBox *circleColorSpinBox;
    QCheckBox *filterByAreaCheckBox;
    QFrame *frame_filter_area;
    QFormLayout *formLayout_2;
    QLabel *label_14;
    QDoubleSpinBox *maxAreaDoubleSpinBox;
    QLabel *label_15;
    QDoubleSpinBox *minAreaDoubleSpinBox;
    QCheckBox *filterByCircularityCheckBox;
    QFrame *frame_filter_circularity;
    QFormLayout *formLayout_3;
    QLabel *label_17;
    QLabel *label_18;
    QDoubleSpinBox *minCircularityDoubleSpinBox;
    QDoubleSpinBox *maxCircularityDoubleSpinBox;
    QCheckBox *filterByInertiaCheckBox;
    QFrame *frame_filter_inertia;
    QFormLayout *formLayout_4;
    QLabel *label_20;
    QDoubleSpinBox *minInertiaRatioDoubleSpinBox;
    QLabel *label_21;
    QDoubleSpinBox *maxInertiaRatioDoubleSpinBox;
    QCheckBox *filterByConvexityCheckBox;
    QFrame *frame_filter_convexity;
    QFormLayout *formLayout;
    QLabel *label_23;
    QDoubleSpinBox *minConvexityDoubleSpinBox;
    QLabel *label_24;
    QDoubleSpinBox *maxConvexityDoubleSpinBox;

    void setupUi(QWidget *ModifiedCircleGridTargetFinder)
    {
        if (ModifiedCircleGridTargetFinder->objectName().isEmpty())
            ModifiedCircleGridTargetFinder->setObjectName(QString::fromUtf8("ModifiedCircleGridTargetFinder"));
        ModifiedCircleGridTargetFinder->resize(493, 631);
        verticalLayout_2 = new QVBoxLayout(ModifiedCircleGridTargetFinder);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        scrollArea = new QScrollArea(ModifiedCircleGridTargetFinder);
        scrollArea->setObjectName(QString::fromUtf8("scrollArea"));
        scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName(QString::fromUtf8("scrollAreaWidgetContents"));
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 459, 1005));
        verticalLayout = new QVBoxLayout(scrollAreaWidgetContents);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        frame = new QFrame(scrollAreaWidgetContents);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        formLayout_5 = new QFormLayout(frame);
        formLayout_5->setObjectName(QString::fromUtf8("formLayout_5"));
        label = new QLabel(frame);
        label->setObjectName(QString::fromUtf8("label"));

        formLayout_5->setWidget(0, QFormLayout::LabelRole, label);

        rowSpinBox = new QSpinBox(frame);
        rowSpinBox->setObjectName(QString::fromUtf8("rowSpinBox"));
        rowSpinBox->setMinimum(1);

        formLayout_5->setWidget(0, QFormLayout::FieldRole, rowSpinBox);

        label_2 = new QLabel(frame);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout_5->setWidget(1, QFormLayout::LabelRole, label_2);

        colSpinBox = new QSpinBox(frame);
        colSpinBox->setObjectName(QString::fromUtf8("colSpinBox"));
        colSpinBox->setMinimum(1);

        formLayout_5->setWidget(1, QFormLayout::FieldRole, colSpinBox);

        label_3 = new QLabel(frame);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        formLayout_5->setWidget(2, QFormLayout::LabelRole, label_3);

        spacingDoubleSpinBox = new QDoubleSpinBox(frame);
        spacingDoubleSpinBox->setObjectName(QString::fromUtf8("spacingDoubleSpinBox"));
        spacingDoubleSpinBox->setDecimals(6);
        spacingDoubleSpinBox->setMaximum(1000000000.000000000000000);
        spacingDoubleSpinBox->setSingleStep(0.010000000000000);

        formLayout_5->setWidget(2, QFormLayout::FieldRole, spacingDoubleSpinBox);


        verticalLayout->addWidget(frame);

        groupBox_5 = new QGroupBox(scrollAreaWidgetContents);
        groupBox_5->setObjectName(QString::fromUtf8("groupBox_5"));
        formLayout_6 = new QFormLayout(groupBox_5);
        formLayout_6->setObjectName(QString::fromUtf8("formLayout_6"));
        label_8 = new QLabel(groupBox_5);
        label_8->setObjectName(QString::fromUtf8("label_8"));

        formLayout_6->setWidget(0, QFormLayout::LabelRole, label_8);

        circleInclusionRadiusDoubleSpinBox = new QDoubleSpinBox(groupBox_5);
        circleInclusionRadiusDoubleSpinBox->setObjectName(QString::fromUtf8("circleInclusionRadiusDoubleSpinBox"));
        circleInclusionRadiusDoubleSpinBox->setDecimals(6);
        circleInclusionRadiusDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_6->setWidget(0, QFormLayout::FieldRole, circleInclusionRadiusDoubleSpinBox);

        label_9 = new QLabel(groupBox_5);
        label_9->setObjectName(QString::fromUtf8("label_9"));

        formLayout_6->setWidget(1, QFormLayout::LabelRole, label_9);

        label_10 = new QLabel(groupBox_5);
        label_10->setObjectName(QString::fromUtf8("label_10"));

        formLayout_6->setWidget(2, QFormLayout::LabelRole, label_10);

        maxRadiusDiffDoubleSpinBox = new QDoubleSpinBox(groupBox_5);
        maxRadiusDiffDoubleSpinBox->setObjectName(QString::fromUtf8("maxRadiusDiffDoubleSpinBox"));
        maxRadiusDiffDoubleSpinBox->setDecimals(6);
        maxRadiusDiffDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_6->setWidget(1, QFormLayout::FieldRole, maxRadiusDiffDoubleSpinBox);

        maxAvgEllipseErrorDoubleSpinBox = new QDoubleSpinBox(groupBox_5);
        maxAvgEllipseErrorDoubleSpinBox->setObjectName(QString::fromUtf8("maxAvgEllipseErrorDoubleSpinBox"));
        maxAvgEllipseErrorDoubleSpinBox->setDecimals(6);
        maxAvgEllipseErrorDoubleSpinBox->setMaximum(1.000000000000000);

        formLayout_6->setWidget(2, QFormLayout::FieldRole, maxAvgEllipseErrorDoubleSpinBox);


        verticalLayout->addWidget(groupBox_5);

        groupBox = new QGroupBox(scrollAreaWidgetContents);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        formLayout_9 = new QFormLayout(groupBox);
        formLayout_9->setObjectName(QString::fromUtf8("formLayout_9"));
        label_4 = new QLabel(groupBox);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        formLayout_9->setWidget(0, QFormLayout::LabelRole, label_4);

        minThresholdSpinBox = new QSpinBox(groupBox);
        minThresholdSpinBox->setObjectName(QString::fromUtf8("minThresholdSpinBox"));
        minThresholdSpinBox->setMaximum(255);

        formLayout_9->setWidget(0, QFormLayout::FieldRole, minThresholdSpinBox);

        label_5 = new QLabel(groupBox);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        formLayout_9->setWidget(1, QFormLayout::LabelRole, label_5);

        maxThresholdSpinBox = new QSpinBox(groupBox);
        maxThresholdSpinBox->setObjectName(QString::fromUtf8("maxThresholdSpinBox"));
        maxThresholdSpinBox->setMaximum(255);
        maxThresholdSpinBox->setValue(255);

        formLayout_9->setWidget(1, QFormLayout::FieldRole, maxThresholdSpinBox);

        label_6 = new QLabel(groupBox);
        label_6->setObjectName(QString::fromUtf8("label_6"));

        formLayout_9->setWidget(2, QFormLayout::LabelRole, label_6);

        numThresholdSpinBox = new QSpinBox(groupBox);
        numThresholdSpinBox->setObjectName(QString::fromUtf8("numThresholdSpinBox"));
        numThresholdSpinBox->setMinimum(0);
        numThresholdSpinBox->setMaximum(1000000000);
        numThresholdSpinBox->setValue(10);

        formLayout_9->setWidget(2, QFormLayout::FieldRole, numThresholdSpinBox);

        label_7 = new QLabel(groupBox);
        label_7->setObjectName(QString::fromUtf8("label_7"));

        formLayout_9->setWidget(3, QFormLayout::LabelRole, label_7);

        minRepeatSpinBox = new QSpinBox(groupBox);
        minRepeatSpinBox->setObjectName(QString::fromUtf8("minRepeatSpinBox"));
        minRepeatSpinBox->setMinimum(1);
        minRepeatSpinBox->setMaximum(1000000000);

        formLayout_9->setWidget(3, QFormLayout::FieldRole, minRepeatSpinBox);


        verticalLayout->addWidget(groupBox);

        filterByColorCheckBox = new QCheckBox(scrollAreaWidgetContents);
        filterByColorCheckBox->setObjectName(QString::fromUtf8("filterByColorCheckBox"));

        verticalLayout->addWidget(filterByColorCheckBox);

        frame_filter_color = new QFrame(scrollAreaWidgetContents);
        frame_filter_color->setObjectName(QString::fromUtf8("frame_filter_color"));
        frame_filter_color->setFrameShape(QFrame::StyledPanel);
        frame_filter_color->setFrameShadow(QFrame::Raised);
        formLayout_7 = new QFormLayout(frame_filter_color);
        formLayout_7->setObjectName(QString::fromUtf8("formLayout_7"));
        label_12 = new QLabel(frame_filter_color);
        label_12->setObjectName(QString::fromUtf8("label_12"));

        formLayout_7->setWidget(0, QFormLayout::LabelRole, label_12);

        circleColorSpinBox = new QSpinBox(frame_filter_color);
        circleColorSpinBox->setObjectName(QString::fromUtf8("circleColorSpinBox"));
        circleColorSpinBox->setMinimum(0);
        circleColorSpinBox->setMaximum(255);

        formLayout_7->setWidget(0, QFormLayout::FieldRole, circleColorSpinBox);


        verticalLayout->addWidget(frame_filter_color);

        filterByAreaCheckBox = new QCheckBox(scrollAreaWidgetContents);
        filterByAreaCheckBox->setObjectName(QString::fromUtf8("filterByAreaCheckBox"));

        verticalLayout->addWidget(filterByAreaCheckBox);

        frame_filter_area = new QFrame(scrollAreaWidgetContents);
        frame_filter_area->setObjectName(QString::fromUtf8("frame_filter_area"));
        frame_filter_area->setFrameShape(QFrame::StyledPanel);
        frame_filter_area->setFrameShadow(QFrame::Raised);
        formLayout_2 = new QFormLayout(frame_filter_area);
        formLayout_2->setObjectName(QString::fromUtf8("formLayout_2"));
        label_14 = new QLabel(frame_filter_area);
        label_14->setObjectName(QString::fromUtf8("label_14"));

        formLayout_2->setWidget(0, QFormLayout::LabelRole, label_14);

        maxAreaDoubleSpinBox = new QDoubleSpinBox(frame_filter_area);
        maxAreaDoubleSpinBox->setObjectName(QString::fromUtf8("maxAreaDoubleSpinBox"));
        maxAreaDoubleSpinBox->setDecimals(6);
        maxAreaDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(0, QFormLayout::FieldRole, maxAreaDoubleSpinBox);

        label_15 = new QLabel(frame_filter_area);
        label_15->setObjectName(QString::fromUtf8("label_15"));

        formLayout_2->setWidget(1, QFormLayout::LabelRole, label_15);

        minAreaDoubleSpinBox = new QDoubleSpinBox(frame_filter_area);
        minAreaDoubleSpinBox->setObjectName(QString::fromUtf8("minAreaDoubleSpinBox"));
        minAreaDoubleSpinBox->setDecimals(6);
        minAreaDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_2->setWidget(1, QFormLayout::FieldRole, minAreaDoubleSpinBox);


        verticalLayout->addWidget(frame_filter_area);

        filterByCircularityCheckBox = new QCheckBox(scrollAreaWidgetContents);
        filterByCircularityCheckBox->setObjectName(QString::fromUtf8("filterByCircularityCheckBox"));

        verticalLayout->addWidget(filterByCircularityCheckBox);

        frame_filter_circularity = new QFrame(scrollAreaWidgetContents);
        frame_filter_circularity->setObjectName(QString::fromUtf8("frame_filter_circularity"));
        frame_filter_circularity->setFrameShape(QFrame::StyledPanel);
        frame_filter_circularity->setFrameShadow(QFrame::Raised);
        formLayout_3 = new QFormLayout(frame_filter_circularity);
        formLayout_3->setObjectName(QString::fromUtf8("formLayout_3"));
        label_17 = new QLabel(frame_filter_circularity);
        label_17->setObjectName(QString::fromUtf8("label_17"));

        formLayout_3->setWidget(0, QFormLayout::LabelRole, label_17);

        label_18 = new QLabel(frame_filter_circularity);
        label_18->setObjectName(QString::fromUtf8("label_18"));

        formLayout_3->setWidget(1, QFormLayout::LabelRole, label_18);

        minCircularityDoubleSpinBox = new QDoubleSpinBox(frame_filter_circularity);
        minCircularityDoubleSpinBox->setObjectName(QString::fromUtf8("minCircularityDoubleSpinBox"));
        minCircularityDoubleSpinBox->setDecimals(6);
        minCircularityDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_3->setWidget(0, QFormLayout::FieldRole, minCircularityDoubleSpinBox);

        maxCircularityDoubleSpinBox = new QDoubleSpinBox(frame_filter_circularity);
        maxCircularityDoubleSpinBox->setObjectName(QString::fromUtf8("maxCircularityDoubleSpinBox"));
        maxCircularityDoubleSpinBox->setDecimals(6);
        maxCircularityDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_3->setWidget(1, QFormLayout::FieldRole, maxCircularityDoubleSpinBox);


        verticalLayout->addWidget(frame_filter_circularity);

        filterByInertiaCheckBox = new QCheckBox(scrollAreaWidgetContents);
        filterByInertiaCheckBox->setObjectName(QString::fromUtf8("filterByInertiaCheckBox"));

        verticalLayout->addWidget(filterByInertiaCheckBox);

        frame_filter_inertia = new QFrame(scrollAreaWidgetContents);
        frame_filter_inertia->setObjectName(QString::fromUtf8("frame_filter_inertia"));
        frame_filter_inertia->setFrameShape(QFrame::StyledPanel);
        frame_filter_inertia->setFrameShadow(QFrame::Raised);
        formLayout_4 = new QFormLayout(frame_filter_inertia);
        formLayout_4->setObjectName(QString::fromUtf8("formLayout_4"));
        label_20 = new QLabel(frame_filter_inertia);
        label_20->setObjectName(QString::fromUtf8("label_20"));

        formLayout_4->setWidget(0, QFormLayout::LabelRole, label_20);

        minInertiaRatioDoubleSpinBox = new QDoubleSpinBox(frame_filter_inertia);
        minInertiaRatioDoubleSpinBox->setObjectName(QString::fromUtf8("minInertiaRatioDoubleSpinBox"));
        minInertiaRatioDoubleSpinBox->setDecimals(6);
        minInertiaRatioDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_4->setWidget(0, QFormLayout::FieldRole, minInertiaRatioDoubleSpinBox);

        label_21 = new QLabel(frame_filter_inertia);
        label_21->setObjectName(QString::fromUtf8("label_21"));

        formLayout_4->setWidget(1, QFormLayout::LabelRole, label_21);

        maxInertiaRatioDoubleSpinBox = new QDoubleSpinBox(frame_filter_inertia);
        maxInertiaRatioDoubleSpinBox->setObjectName(QString::fromUtf8("maxInertiaRatioDoubleSpinBox"));
        maxInertiaRatioDoubleSpinBox->setDecimals(6);
        maxInertiaRatioDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout_4->setWidget(1, QFormLayout::FieldRole, maxInertiaRatioDoubleSpinBox);


        verticalLayout->addWidget(frame_filter_inertia);

        filterByConvexityCheckBox = new QCheckBox(scrollAreaWidgetContents);
        filterByConvexityCheckBox->setObjectName(QString::fromUtf8("filterByConvexityCheckBox"));

        verticalLayout->addWidget(filterByConvexityCheckBox);

        frame_filter_convexity = new QFrame(scrollAreaWidgetContents);
        frame_filter_convexity->setObjectName(QString::fromUtf8("frame_filter_convexity"));
        frame_filter_convexity->setFrameShape(QFrame::StyledPanel);
        frame_filter_convexity->setFrameShadow(QFrame::Raised);
        formLayout = new QFormLayout(frame_filter_convexity);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        label_23 = new QLabel(frame_filter_convexity);
        label_23->setObjectName(QString::fromUtf8("label_23"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label_23);

        minConvexityDoubleSpinBox = new QDoubleSpinBox(frame_filter_convexity);
        minConvexityDoubleSpinBox->setObjectName(QString::fromUtf8("minConvexityDoubleSpinBox"));
        minConvexityDoubleSpinBox->setDecimals(6);
        minConvexityDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout->setWidget(0, QFormLayout::FieldRole, minConvexityDoubleSpinBox);

        label_24 = new QLabel(frame_filter_convexity);
        label_24->setObjectName(QString::fromUtf8("label_24"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label_24);

        maxConvexityDoubleSpinBox = new QDoubleSpinBox(frame_filter_convexity);
        maxConvexityDoubleSpinBox->setObjectName(QString::fromUtf8("maxConvexityDoubleSpinBox"));
        maxConvexityDoubleSpinBox->setDecimals(6);
        maxConvexityDoubleSpinBox->setMaximum(1000000000.000000000000000);

        formLayout->setWidget(1, QFormLayout::FieldRole, maxConvexityDoubleSpinBox);


        verticalLayout->addWidget(frame_filter_convexity);

        scrollArea->setWidget(scrollAreaWidgetContents);

        verticalLayout_2->addWidget(scrollArea);


        retranslateUi(ModifiedCircleGridTargetFinder);

        QMetaObject::connectSlotsByName(ModifiedCircleGridTargetFinder);
    } // setupUi

    void retranslateUi(QWidget *ModifiedCircleGridTargetFinder)
    {
        ModifiedCircleGridTargetFinder->setWindowTitle(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Form", nullptr));
        label->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Rows", nullptr));
        label_2->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Cols", nullptr));
        label_3->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Spacing (m)", nullptr));
        groupBox_5->setTitle(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Circle Fit", nullptr));
        label_8->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Circle Inclusion Radius (px)", nullptr));
        label_9->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Radius Diff  (px)", nullptr));
        label_10->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Avg Ellipse Error (px)", nullptr));
        groupBox->setTitle(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Thresholds", nullptr));
        label_4->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Minimum", nullptr));
        label_5->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max", nullptr));
        label_6->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Number", nullptr));
        label_7->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Repeatability", nullptr));
        filterByColorCheckBox->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Filter By Color", nullptr));
        label_12->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Circle Color", nullptr));
        filterByAreaCheckBox->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Filter by Area", nullptr));
        label_14->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Min Area (px^2)", nullptr));
        label_15->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Area (px^2)", nullptr));
        filterByCircularityCheckBox->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Filter by Circularity", nullptr));
        label_17->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Min Circularity", nullptr));
        label_18->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Circularity", nullptr));
        filterByInertiaCheckBox->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Filter by Inertia", nullptr));
        label_20->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Min Inertia Ratio", nullptr));
        label_21->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Inertia Ratio", nullptr));
        filterByConvexityCheckBox->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Filter by Convexity", nullptr));
        label_23->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Min Convexity", nullptr));
        label_24->setText(QCoreApplication::translate("ModifiedCircleGridTargetFinder", "Max Convexity", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ModifiedCircleGridTargetFinder: public Ui_ModifiedCircleGridTargetFinder {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MODIFIED_CIRCLE_GRID_TARGET_FINDER_H
