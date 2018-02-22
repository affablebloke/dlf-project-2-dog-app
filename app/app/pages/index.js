import React from 'react'
import Link from 'next/link'
import { Clipboard, Cpu } from 'react-feather';

export default class Index extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      photo: null,
      isProcessing: false,
      prediction: null
    };
  }

  onUploadPhoto = evt => {
    window.URL = window.URL || window.webkitURL;
    this.setState({ photo: evt.target.files[0], photoUrl: window.URL.createObjectURL(evt.target.files[0]), isProcessing: true });
    const xhr = new XMLHttpRequest();

    const that = this;
    xhr.upload.addEventListener("progress", function (e) {
      if (e.lengthComputable) {
        const percentage = Math.round((e.loaded * 100) / e.total);
      }
    }, false);

    xhr.onload = (e) => {
      // that.ctrl.update(100);
      // console.log(JSON.parse(xhr.response));
      that.setState({ isProcessing: false, prediction: JSON.parse(xhr.response) }); // remove this later

    };
    xhr.open("POST", "http://localhost:5000/api/predict", true);
    // xhr.withCredentials = true;
    xhr.send(evt.target.files[0]);
  }

  onClickPhotoInput = () => {
    this.photoFileInput.click()
  }

  render() {
    const { photo, photoUrl, isProcessing, prediction } = this.state;
    return (
      <div className="container">
        <div className="title-container">
          <Clipboard style={{ alignSelf: 'center', marginRight: '.5em' }} />
          <h1>DLF Project 2: Dog Breed Classifier</h1>
        </div>
        {photoUrl &&
          <img className="img-container" src={photoUrl} />}
        {isProcessing && <div className="image-container">
          <p style={{fontSize: '1.5em', color: 'white'}}><Cpu /> Processing image....</p>
        </div>}
        {prediction && !isProcessing && <div className="prediction-container">
          { !prediction.error && <p className="assumption">{prediction.is_dog ? `This dog looks like a....` : `This human looks like a....`}</p> }
          <a target="_blank" href={`https://www.google.com/search?q=${prediction.breed}`} className="breed-name">{prediction.breed}</a>
          { prediction.error && <p className="assumption">The image provided does not resemble a human or dog!</p> }
        </div>}
        <div className="button-container">
          <form encType="multipart/form-data" name="remittance-form">
            {!isProcessing && <label className="button" htmlFor="photo">{photoUrl ? `Classify Another Photo` : `Upload and Classify Photo`}<input id="photo" style={{ display: 'none' }} accept="image/*" onChange={this.onUploadPhoto} type="file" name="photo" ref={(input) => { this.photoFileInput = input; }} /></label>}
          </form>
        </div>
        <style jsx>{`
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Roboto;
            text-decoration: none;
        }
        h1{
          font-size: 1.5em;
        }
        .img-container{
          width: 350px;
          object-fit: contain;
          align-self: center;
          margin-top: 2.0em;
          box-shadow: 1px 1px 5px rgba(0,0,0,.35);
        }
        .title-container{
          padding: 10px;
          display: flex;
          flex: 1;
          justify-content: center;
          flex-direction: row;
          color: white;
          background-color: rgba(0,0,0,.05);
          border-bottom: 1px solid rgba(0,0,0,.20);
        }
        .button-container{
          margin: 4.0em;
          display: flex;
          flex-direction: row;
          justify-content: center;
        }
        .image-container{
          margin-top: 2.0em;
          display: flex;
          flex-direction: row;
          justify-content: center;
        }
        .prediction-container{
          margin-top: 2.0em;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          align-self: center;
          color: white;
          padding: 1.5em;
        }
        .prediction-container a{
          color: white;
          text-decoration: underline;
        }
        .prediction-container a:active{
          color: #white;
        }
        .breed-name{
          font-size: 2.0em;
          text-transform: capitalize;
        }
        .assumption{
          font-size: 1.25em;
        }
        .button{
          background-color: #2196f3;
          border-radius: 2.0em;
          padding: 1em 2em;
          color: white;
          cursor: pointer;
          box-shadow: 1px 1px 5px rgba(0,0,0,.25);
        }
        .container {
          margin: 0;
          padding: 0;
          display: flex;
          flex: 1;
          flex-direction: column;
        }
    `}</style>
      </div>
    )
  }

}