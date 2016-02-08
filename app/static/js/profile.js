/*
$(document).ready(function() {
$(".btn-pref .btn").click(function () {
    $(".btn-pref .btn").removeClass("btn-primary").addClass("btn-default");
    $(".tab").addClass("active"); // instead of this do the below 
    $(this).removeClass("btn-default").addClass("btn-primary");   
});
});

*/
var ButtonToolbar = ReactBootstrap.ButtonToolbar;
var Modal = ReactBootstrap.Modal;
var Button = ReactBootstrap.Button;
var buttonsInstance = (
    <ButtonToolbar>
      <Button>Default</Button>
    </ButtonToolbar>
  );

const uploadModal = React.createClass({
	getInitialStatus() {
		return {show: false};
	},

	render() {
		"use strict";
		let close = () => this.setState({show: false});	
		
		return (
			<div className="modal-container" style={{height: 200}}>
				<Button 
					bsSize="small"
					onClick={() => this.setState({show: true})}>
				edit
				</Button>

				<Modal 
					show={this.state.show}
					onHide={close}
					container={this}
					aria-labelledby="contained-modal-title">
				
					<Modal.Header closeButton>
						<Modal.Title id="contained-modal-title">写真アップロード</Modal.Title>
					</Modal.Header>
					<Modal.Body>
						<form action="/avatar" method="post" enctype="multipart/form-data">
							<input type="file" name="avatar"/>
							<input type="submit" value="アップロード"/>
						</form>
					</Modal.Body>
					<Modal.Footer>
						<Button 
							onClick={close}>閉じる
						</Button>
					</Modal.Footer>
				</Modal>
			</div>
		);
	}
});

React.render(
	React.createElement(uploadModal, null),
	document.getElementById('edit-btn')
);


			
