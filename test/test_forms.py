from pathlib import Path
from unittest.mock import Mock, patch

from py_utils.forms import pic_dir, pic_file


@patch("py_utils.forms.filedialog.askdirectory", return_value="/mocked/path")
@patch("py_utils.forms.tk.Tk")
def test_pic_dir(mock_tk, mock_dialog) -> None:
    # Ensures Tk root is created and destroyed cleanly
    mock_root = Mock()
    mock_tk.return_value = mock_root
    
    res = pic_dir(Path("/home"))
    
    assert isinstance(res, Path)
    assert str(res) == "/mocked/path"
    mock_root.withdraw.assert_called_once()
    mock_root.destroy.assert_called_once()


@patch("py_utils.forms.filedialog.askopenfilename", return_value="")
@patch("py_utils.forms.tk.Tk")
def test_pic_file_cancel(mock_tk, mock_dialog) -> None:
    # Tests cancellation returning None
    res = pic_file(Path("/home"))
    assert res is None