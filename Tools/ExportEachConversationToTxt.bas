Attribute VB_Name = "ExportEachConversationToTxt"
Option Explicit

Sub ExportEachConversationToTxt()
    Dim oSel As Outlook.Selection
    Dim oMail As Outlook.MailItem
    Dim sPath As String
    Dim sFile As String
    Dim sBase As String
    Dim sSubject As String
    Dim sDate As String
    Dim iFile As Integer
    Dim i As Long
    Dim iCount As Long
    Dim iFailed As Long
    Dim nDup As Long
    Dim aChar As Variant

    ' --- Validate selection first ---
    Set oSel = Application.ActiveExplorer.Selection
    If oSel.Count = 0 Then
        MsgBox "No items selected.", vbExclamation
        Exit Sub
    End If

    ' --- Configure export folder ---
    sPath = CreateObject("WScript.Shell").SpecialFolders("MyDocuments") & "\OutlookExport\"
    If Dir(sPath, vbDirectory) = "" Then MkDir sPath

    iCount = 0
    iFailed = 0

    For i = 1 To oSel.Count
        ' Keep Outlook responsive during large exports
        If i Mod 25 = 0 Then DoEvents

        If oSel(i).Class <> olMail Then GoTo NextItem
        Set oMail = oSel(i)

        ' --- Build safe filename ---
        sSubject = oMail.Subject
        If Len(Trim(sSubject)) = 0 Then sSubject = "(no subject)"

        ' Strip Windows-illegal filename characters
        For Each aChar In Array("\", "/", ":", "*", "?", """", "<", ">", "|")
            sSubject = Replace(sSubject, aChar, "-")
        Next aChar
        sSubject = Trim(sSubject)

        ' Guard against empty/unset SentOn (Outlook uses 1/1/4501 for unset dates)
        If Year(oMail.SentOn) < 2100 And oMail.SentOn > 0 Then
            sDate = Format(oMail.SentOn, "yyyy-mm-dd")
        Else
            sDate = "0000-00-00"
        End If

        sBase = sPath & sDate & " - " & Left(sSubject, 60)

        ' Resolve duplicate filenames by appending a counter
        sFile = sBase & ".txt"
        nDup = 1
        Do While Len(Dir(sFile)) > 0
            nDup = nDup + 1
            sFile = sBase & " (" & nDup & ").txt"
        Loop

        ' --- Write file (per-item error handling — one failure won't stop the batch) ---
        On Error Resume Next
        Err.Clear

        iFile = FreeFile
        Open sFile For Output As #iFile
        If Err.Number <> 0 Then
            iFailed = iFailed + 1
            Err.Clear
            On Error GoTo 0
            GoTo NextItem
        End If

        Print #iFile, "Subject:    " & oMail.Subject
        Print #iFile, "From:       " & oMail.SenderName & " <" & oMail.SenderEmailAddress & ">"
        Print #iFile, "To:         " & oMail.To
        Print #iFile, "CC:         " & oMail.CC
        Print #iFile, "Sent:       " & Format(oMail.SentOn, "yyyy-mm-dd hh:nn:ss")
        Print #iFile, "Categories: " & oMail.Categories
        Print #iFile, String(60, "-")
        Print #iFile, oMail.Body

        Close #iFile

        If Err.Number <> 0 Then
            iFailed = iFailed + 1
            Err.Clear
        Else
            iCount = iCount + 1
        End If
        On Error GoTo 0

NextItem:
        Set oMail = Nothing
    Next i

    ' --- Summary ---
    Dim sMsg As String
    sMsg = "Export complete." & vbCrLf & vbCrLf _
         & "Exported:  " & iCount & " file(s)" & vbCrLf _
         & "Failed:    " & iFailed & " file(s)" & vbCrLf _
         & "Skipped:   " & (oSel.Count - iCount - iFailed) & " non-mail item(s)" & vbCrLf _
         & vbCrLf & "Folder: " & sPath

    MsgBox sMsg, vbInformation

    Set oSel = Nothing
End Sub
