// MFC-UCL-MI3-SettingsDlg.cpp : IMPLEMENTATION FILE
// Author: Anelia Gaydardzhieva
#include "pch.h"
#include "math.h"
#include "framework.h"
#include "MFC-UCL-MI3-Settings.h"
#include "MFC-UCL-MI3-SettingsDlg.h"
#include "afxdialogex.h"
#include <Windows.h>
#include <filesystem>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include "../packages/nlohmann.json.3.10.5/build/native/include/nlohmann/json.hpp"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// define json library
using json = nlohmann::json;
using namespace std;

// define global variables
string globalCurrentMode;
int globalMaxNumHands;
bool globalSpeech;
int globalCameraNr;
double globalSensitivity;
bool globalShowFPS;

// Define grids
#define MODE_LEFT_SWIPE "kiosk_swipe_left_hand"
#define MODE_RIGHT_SWIPE "kiosk_swipe_right_hand"

//parameters

#define MAX_CAMERA_INDEX 9

// CMFCUCLMI3SettingsDlg Dialog - MFC VARIABLES
CMFCUCLMI3SettingsDlg::CMFCUCLMI3SettingsDlg(CWnd* pParent) : CDialogEx(IDD_MFCUCLMI3SETTINGS_DIALOG, pParent) {
	//UCL LOGO ICON
	m_hIcon = AfxGetApp()->LoadIcon(IDI_ICON1);
	// uncomment below for the MFC default logo (and comment the line above)
	//m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMFCUCLMI3SettingsDlg::DoDataExchange(CDataExchange* pDX) {
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_DEFAULTCAMERA_COMBO, m_camera);
	DDX_Control(pDX, IDC_HANDCONTROL_LEFT_BUTTON, m_handLeft);
	DDX_Control(pDX, IDC_HANDCONTROL_RIGHT_BUTTON, m_handRight);
	DDX_Control(pDX, IDC_SWIPE_SENSITIVITY_SLIDER, m_sensitivity);
	DDX_Control(pDX, IDC_SWIPE_SENSITIVITY_COUNTER, m_sensitivityValue);
	DDX_Control(pDX, IDC_MAXNUMHANDS_SLIDER, m_maxnumhands);
	DDX_Control(pDX, IDC_MAXNUMHANDS_COUNTER, m_maxnumhandsValue);
}

BEGIN_MESSAGE_MAP(CMFCUCLMI3SettingsDlg, CDialogEx)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDOK, &CMFCUCLMI3SettingsDlg::Save)
	ON_WM_HSCROLL()
	ON_WM_HSCROLL()
	ON_BN_CLICKED(IDC_HANDCONTROL_LEFT_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateHandLeft)
	ON_BN_CLICKED(IDC_HANDCONTROL_RIGHT_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateHandRight)
	ON_BN_CLICKED(IDC_BUTTON_INFO_HANDCONTROL, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoHandControl)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SWIPESENSITIVITY, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSensitivity)
	ON_BN_CLICKED(IDC_BUTTON_INFO_MAXNUMHANDS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMaxNumHands)
	ON_BN_CLICKED(IDC_BUTTON_INFO_DEFAULT_CAMERA, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoDefaultCamera)
	ON_BN_CLICKED(IDC_BUTTON_EXIT_MOTIONINPUT, &CMFCUCLMI3SettingsDlg::OnClickedButtonExitMotioninput)
END_MESSAGE_MAP()

// drag window cursor
HCURSOR CMFCUCLMI3SettingsDlg::OnQueryDragIcon() {
	return static_cast<HCURSOR>(m_hIcon);
}

// Paint
void CMFCUCLMI3SettingsDlg::OnPaint() {
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting
		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);
		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;
		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}


// Init
BOOL CMFCUCLMI3SettingsDlg::OnInitDialog() {
	CDialogEx::OnInitDialog();

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	//SetIcon(m_hIcon, FALSE);		// Set small icon


	// CONFIG data
	wstring pathConfigS = L"MotionInput\\data\\config.json";
	LPCWSTR pathConfig = pathConfigS.c_str();

	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));

	json myjson_config = json::parse(content_config);
	auto& general = myjson_config["general"];
	auto& modules = myjson_config["modules"];
	auto& events = myjson_config["events"];

	// JSON MODES PATH
	wstring pathModesS = L"MotionInput\\data\\mode_controller.json";
	LPCWSTR pathModes = pathModesS.c_str();

	ifstream ifs_modes(pathModes);
	string content_modes((istreambuf_iterator<char>(ifs_modes)), (istreambuf_iterator<char>()));

	json myjson_modes = json::parse(content_modes);
	auto& current_mode = MODE_RIGHT_SWIPE;

	// Set mode data
	globalCurrentMode = current_mode;
	m_handLeft.SetCheck(current_mode == MODE_LEFT_SWIPE);
	m_handRight.SetCheck(current_mode == MODE_RIGHT_SWIPE);


	// Set config data
	globalShowFPS = general["view"]["show_fps"]; // FPS
	globalSpeech = modules["speech"]["enabled"]; // SPEECH
	globalSensitivity = events["kiosk_swipe"]["swipe_sensitivity"]; // SENSITIVITY
	globalCameraNr = general["camera"]["camera_nr"]; // CAMERA
	globalMaxNumHands = 2; // MAX NUMBER OF HANDS


	CString strSliderValue;
	m_sensitivity.SetRange(0, 100);
	m_sensitivity.SetPos(globalSensitivity * 100);
	strSliderValue.Format(_T("%d"), int(globalSensitivity * 100));
	m_sensitivityValue.SetWindowText(strSliderValue);

	CString strMaxnumhandsSliderValue;
	m_maxnumhands.SetRange(1, 10);
	m_maxnumhands.SetPos(globalMaxNumHands);
	strMaxnumhandsSliderValue.Format(_T("%d"), int(globalMaxNumHands));
	m_maxnumhandsValue.SetWindowText(strMaxnumhandsSliderValue);

	// Camera
	for (int i = 0; i < MAX_CAMERA_INDEX; i++)
	{
		CString curIndex;
		curIndex.Format(_T("Camera %d"), i + 1);
		m_camera.AddString(curIndex);
	}
	m_camera.SetCurSel(globalCameraNr);

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save
void CMFCUCLMI3SettingsDlg::Save() {
	// Update values
	if (m_handLeft.GetCheck()) globalCurrentMode = MODE_LEFT_SWIPE;
	else if (m_handRight.GetCheck()) globalCurrentMode = MODE_RIGHT_SWIPE;

	globalSensitivity = m_sensitivity.GetPos();
	globalMaxNumHands = m_maxnumhands.GetPos();
	globalCameraNr = m_camera.GetCurSel();


	// --------------------- WRITE JSON ---------------------

	// Save Modes
	wstring tempStrModes = L"MotionInput\\data\\mode_controller.json";
	LPCWSTR pathModes = tempStrModes.c_str();
	ifstream ifs_modes(pathModes);
	string content_modes((istreambuf_iterator<char>(ifs_modes)), (istreambuf_iterator<char>()));
	json myjson_modes = json::parse(content_modes);
	myjson_modes["current_mode"] = globalCurrentMode;

	ofstream outputModesFile(pathModes);
	outputModesFile << setw(4) << myjson_modes << endl;

	// Save Configs
	wstring tempStrConfig = L"MotionInput\\data\\configMFC.json";
	LPCWSTR pathConfig = tempStrConfig.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json myjson_config = json::parse(content_config);
	auto& general = myjson_config["general"];
	auto& modules = myjson_config["modules"];
	auto& events = myjson_config["events"];
	events["kiosk_swipe"]["swipe_sensitivity"] = globalSensitivity / 100;
	general["camera"]["camera_nr"] = globalCameraNr;
	general["zeromq_client_enabled"] = true;
	modules["hand"]["max_num_hands"] = globalMaxNumHands;


	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << myjson_config << endl;

	//MessageBox(_T("UCL MotionInput will now restart and apply the new setting."), _T("Information"));
	MessageBox(_T("Any changes made have now been saved.\n\nMotionInput will now be restarted to apply the new settings."), _T("Changes Saved"));

	// 1. Exit MI
	WinExec("TASKKILL /IM motioninput_api.exe /t /f", SW_HIDE);
	WinExec("TASKKILL /IM motioninput_server.exe /t /f", SW_HIDE);

	// 2. Copy amended configMFC.json file from MFC app to config.json
	Sleep(1000);	// 1 seconds delay
	ifstream src(L"MotionInput\\data\\configMFC.json", ios::binary);
	ofstream dst(L"MotionInput\\data\\config.json", ios::binary);
	dst << src.rdbuf();

	// 3. Run MI server again
	wstring tempStr = L"MotionInputServer\\motioninput_server.exe";
	LPCWSTR finalPythonPath = tempStr.c_str();

	SHELLEXECUTEINFO si = { sizeof(SHELLEXECUTEINFO) };
	si.hwnd = GetSafeHwnd();
	si.lpVerb = L"open";
	si.lpFile = finalPythonPath;
	si.nShow = SW_HIDE;
	ShellExecuteEx(&si);

	// 3. Run MI again
	wstring tempStr2 = L"MotionInput\\motioninput_api.exe";
	LPCWSTR finalPythonPath2 = tempStr2.c_str();

	SHELLEXECUTEINFO si2 = { sizeof(SHELLEXECUTEINFO) };
	si2.hwnd = GetSafeHwnd();
	si2.lpVerb = L"open";
	si2.lpFile = finalPythonPath2;
	si2.nShow = SW_HIDE;
	ShellExecuteEx(&si2);


	// 4. Close the MFC
	//CDialogEx::OnOK();
}

void CMFCUCLMI3SettingsDlg::OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar) {
	CSliderCtrl* pSlider = reinterpret_cast<CSliderCtrl*>(pScrollBar);

	if (pSlider == &m_sensitivity) {
		CString strSliderValue;
		int iValue = m_sensitivity.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_sensitivityValue.SetWindowText(strSliderValue);
	}

	if (pSlider == &m_maxnumhands) {
		CString strMaxnumhandsSliderValue;
		int iValue = m_maxnumhands.GetPos(); // Get Slider value
		strMaxnumhandsSliderValue.Format(_T("%d"), iValue);
		m_maxnumhandsValue.SetWindowText(strMaxnumhandsSliderValue);
	}
}

// Update UI of hand buttons
void CMFCUCLMI3SettingsDlg::UpdateHandLeft() {
	m_handLeft.SetCheck(1);
	m_handRight.SetCheck(0);
}
void CMFCUCLMI3SettingsDlg::UpdateHandRight() {
	m_handLeft.SetCheck(0);
	m_handRight.SetCheck(1);
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoHandControl() {
	MessageBox(_T("Selecting the left or right hand indicates the dominant hand which will be used for controling the view. All hand gestures are done using the selected hand."), _T("Hand Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSensitivity() {
	MessageBox(_T("The swipe gesture gets triggered when you take your hand from the centre of the screen to one of its edges. The swipe sensitivity indicates how close to the screen's edge does the hand need to be in order to trigger a swipe. The higher the sensitivity, the closer the hand needs to be to the screen's edge."), _T("Sensitivity Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMaxNumHands() {
	MessageBox(_T("The maximum number of hands the program can detect. The higher this is, the more hands the program is aware of and the better its choice of the controlling hand. However, setting this higher also makes the program run slower"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoDefaultCamera()
{
	MessageBox(_T("Some computer devices may have two or more webcams available for MotionInput to use (such as Microsoft Surface devices which often have a front and a rear camera). Some users might also prefer attaching an additional camera(s) to their computer devices. \n\nThe default camera value is initially set to 0. If you are experiencing difficulties with MotionInput camera detection, set this option to a different number. In most cases, changing 0 to 1 or 2 is likely to be a solution. \nRestart MotionInput to check if the new number selected has resolved the problem. If not adjust the setting again until MotionInput is connected to the desired camera."), _T("Default Camera Information"));
}

void CMFCUCLMI3SettingsDlg::OnClickedButtonExitMotioninput()
{
	WinExec("TASKKILL /IM motioninput_api.exe /t /f", SW_HIDE);
	WinExec("TASKKILL /IM motioninput_server.exe /t /f", SW_HIDE);
}
