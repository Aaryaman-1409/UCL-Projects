// MFC-UCL-MI3-SettingsDlg.h : HEADER FILE

#pragma once


// CMFCUCLMI3SettingsDlg dialog
class CMFCUCLMI3SettingsDlg : public CDialogEx
{

	// Construction
public:
	CMFCUCLMI3SettingsDlg(CWnd* pParent = nullptr);	// standard constructor

	// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_MFCUCLMI3SETTINGS_DIALOG };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


	// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()

public:
	afx_msg void Save();

	CComboBox m_camera;

	afx_msg void OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);

	CButton m_handLeft;
	CButton m_handRight;
	afx_msg void UpdateHandLeft();
	afx_msg void UpdateHandRight();
	CSliderCtrl m_sensitivity;
	CEdit m_sensitivityValue;
	CSliderCtrl m_maxnumhands;
	CEdit m_maxnumhandsValue;
	afx_msg void OnBnClickedButtonInfoSensitivity();
	afx_msg void OnBnClickedButtonInfoMaxNumHands();
	afx_msg void OnBnClickedButtonInfoHandControl();
	afx_msg void OnBnClickedButtonInfoDefaultCamera();
	afx_msg void OnClickedButtonExitMotioninput();
	afx_msg void OnBnClickedGeneral();
};

